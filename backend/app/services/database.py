"""Small SQLite persistence layer for the single-school AI4Impact MVP."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def database_path() -> Path:
    configured = os.getenv("VERIQ_DB_PATH")
    path = Path(configured) if configured else Path(__file__).resolve().parents[2] / "data" / "veriq_mvp.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(database_path())
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS imports (
                id TEXT PRIMARY KEY,
                school_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                attendance_csv BLOB NOT NULL,
                behaviour_csv BLOB NOT NULL,
                assessments_csv BLOB NOT NULL
            );
            CREATE TABLE IF NOT EXISTS school_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                import_id TEXT NOT NULL REFERENCES imports(id) ON DELETE CASCADE,
                kind TEXT NOT NULL,
                student_id TEXT NOT NULL,
                learner_name TEXT,
                class_name TEXT NOT NULL,
                record_date TEXT NOT NULL,
                status TEXT,
                subject TEXT,
                score REAL,
                incident_type TEXT,
                severity TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_records_import ON school_records(import_id);
            CREATE INDEX IF NOT EXISTS idx_records_scope ON school_records(import_id, class_name, student_id);
            CREATE TABLE IF NOT EXISTS evidence_snapshots (
                analysis_id TEXT PRIMARY KEY,
                import_id TEXT,
                source TEXT NOT NULL,
                created_at TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS decisions (
                id TEXT PRIMARY KEY,
                analysis_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS workspace_settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                school_name TEXT NOT NULL,
                school_location TEXT NOT NULL,
                user_name TEXT NOT NULL,
                user_role TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS beacon_conversations (
                id TEXT PRIMARY KEY,
                analysis_id TEXT NOT NULL,
                title TEXT NOT NULL,
                scope_type TEXT NOT NULL,
                scope_id TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_beacon_conversations_analysis
            ON beacon_conversations(analysis_id, updated_at DESC);
            CREATE TABLE IF NOT EXISTS beacon_turns (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL REFERENCES beacon_conversations(id) ON DELETE CASCADE,
                created_at TEXT NOT NULL,
                question TEXT NOT NULL,
                response_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_beacon_turns_conversation
            ON beacon_turns(conversation_id, created_at);
            """
        )
        record_columns = {row["name"] for row in connection.execute("PRAGMA table_info(school_records)")}
        if "learner_name" not in record_columns:
            connection.execute("ALTER TABLE school_records ADD COLUMN learner_name TEXT")
        connection.execute(
            """INSERT OR IGNORE INTO workspace_settings
            (id, school_name, school_location, user_name, user_role, updated_at)
            VALUES (1, 'Mufakose High', 'Harare, Zimbabwe', 'Tendai Moyo', 'Deputy Head', ?)""",
            (datetime.now(UTC).isoformat(),),
        )


def save_import(
    import_id: str,
    school_name: str,
    files: dict[str, bytes],
    records: list[dict[str, Any]],
) -> None:
    initialize_database()
    now = datetime.now(UTC).isoformat()
    with connect() as connection:
        connection.execute(
            "INSERT INTO imports VALUES (?, ?, ?, ?, ?, ?)",
            (import_id, school_name, now, files["attendance"], files["behaviour"], files["assessments"]),
        )
        connection.executemany(
            """INSERT INTO school_records (
                import_id, kind, student_id, learner_name, class_name, record_date, status,
                subject, score, incident_type, severity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    import_id, row["kind"], row["student_id"], row.get("first_name"), row["class_name"], row["date"],
                    row.get("status"), row.get("subject"), row.get("score"),
                    row.get("incident_type"), row.get("severity"),
                )
                for row in records
            ],
        )


def save_snapshot(snapshot: dict[str, Any], source: str, import_id: str | None = None) -> None:
    initialize_database()
    with connect() as connection:
        connection.execute(
            "INSERT OR REPLACE INTO evidence_snapshots VALUES (?, ?, ?, ?, ?)",
            (
                snapshot["analysis_id"], import_id, source,
                snapshot.get("generated_at", datetime.now(UTC).isoformat()),
                json.dumps(snapshot, ensure_ascii=False),
            ),
        )


def latest_snapshot() -> tuple[dict[str, Any], str] | None:
    initialize_database()
    with connect() as connection:
        row = connection.execute(
            "SELECT payload_json, source FROM evidence_snapshots ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
    if row is None:
        return None
    return json.loads(row["payload_json"]), row["source"]


def save_decision(decision: dict[str, Any]) -> None:
    initialize_database()
    now = datetime.now(UTC).isoformat()
    with connect() as connection:
        connection.execute(
            "INSERT OR REPLACE INTO decisions VALUES (?, ?, COALESCE((SELECT created_at FROM decisions WHERE id = ?), ?), ?, ?)",
            (decision["id"], decision["analysis_id"], decision["id"], now, now, json.dumps(decision, ensure_ascii=False)),
        )


def latest_decision(analysis_id: str | None = None) -> dict[str, Any] | None:
    initialize_database()
    query = "SELECT payload_json FROM decisions"
    params: tuple[Any, ...] = ()
    if analysis_id:
        query += " WHERE analysis_id = ?"
        params = (analysis_id,)
    query += " ORDER BY updated_at DESC LIMIT 1"
    with connect() as connection:
        row = connection.execute(query, params).fetchone()
    return json.loads(row["payload_json"]) if row else None


def update_decision(decision_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
    initialize_database()
    with connect() as connection:
        row = connection.execute("SELECT payload_json FROM decisions WHERE id = ?", (decision_id,)).fetchone()
    if row is None:
        return None
    decision = json.loads(row["payload_json"])
    decision.update(updates)
    save_decision(decision)
    return decision


def get_workspace() -> dict[str, str]:
    initialize_database()
    with connect() as connection:
        row = connection.execute("SELECT * FROM workspace_settings WHERE id = 1").fetchone()
    return {
        "school_name": row["school_name"],
        "school_location": row["school_location"],
        "user_name": row["user_name"],
        "user_role": row["user_role"],
        "updated_at": row["updated_at"],
    }


def update_workspace(updates: dict[str, str]) -> dict[str, str]:
    current = get_workspace()
    current.update(updates)
    current["updated_at"] = datetime.now(UTC).isoformat()
    with connect() as connection:
        connection.execute(
            """UPDATE workspace_settings SET school_name = ?, school_location = ?,
            user_name = ?, user_role = ?, updated_at = ? WHERE id = 1""",
            (current["school_name"], current["school_location"], current["user_name"], current["user_role"], current["updated_at"]),
        )
    return current


def update_latest_snapshot_school(school_name: str) -> None:
    """Keeps the active intelligence context aligned with the saved workspace identity."""
    initialize_database()
    with connect() as connection:
        row = connection.execute(
            "SELECT analysis_id, payload_json FROM evidence_snapshots ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        if row is None:
            return
        payload = json.loads(row["payload_json"])
        payload["school_name"] = school_name
        connection.execute(
            "UPDATE evidence_snapshots SET payload_json = ? WHERE analysis_id = ?",
            (json.dumps(payload, ensure_ascii=False), row["analysis_id"]),
        )


def save_beacon_turn(
    analysis_id: str,
    question: str,
    response: dict[str, Any],
    scope_type: str,
    scope_id: str | None,
    conversation_id: str | None = None,
) -> str:
    """Persists a Beacon exchange and creates a conversation when required."""
    from uuid import uuid4

    initialize_database()
    now = datetime.now(UTC).isoformat()
    conversation_id = conversation_id or f"conversation_{uuid4().hex}"
    with connect() as connection:
        existing = connection.execute(
            "SELECT id FROM beacon_conversations WHERE id = ? AND analysis_id = ?",
            (conversation_id, analysis_id),
        ).fetchone()
        if existing is None:
            title = question.strip()[:80]
            connection.execute(
                "INSERT INTO beacon_conversations VALUES (?, ?, ?, ?, ?, ?, ?)",
                (conversation_id, analysis_id, title, scope_type, scope_id, now, now),
            )
        else:
            connection.execute(
                "UPDATE beacon_conversations SET scope_type = ?, scope_id = ?, updated_at = ? WHERE id = ?",
                (scope_type, scope_id, now, conversation_id),
            )
        connection.execute(
            "INSERT INTO beacon_turns VALUES (?, ?, ?, ?, ?)",
            (f"turn_{uuid4().hex}", conversation_id, now, question, json.dumps(response, ensure_ascii=False)),
        )
    return conversation_id


def list_beacon_conversations(analysis_id: str) -> list[dict[str, Any]]:
    initialize_database()
    with connect() as connection:
        rows = connection.execute(
            """SELECT c.*, COUNT(t.id) AS turn_count
            FROM beacon_conversations c
            LEFT JOIN beacon_turns t ON t.conversation_id = c.id
            WHERE c.analysis_id = ?
            GROUP BY c.id
            ORDER BY c.updated_at DESC LIMIT 20""",
            (analysis_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_beacon_conversation(conversation_id: str, analysis_id: str) -> dict[str, Any] | None:
    initialize_database()
    with connect() as connection:
        conversation = connection.execute(
            "SELECT * FROM beacon_conversations WHERE id = ? AND analysis_id = ?",
            (conversation_id, analysis_id),
        ).fetchone()
        if conversation is None:
            return None
        turns = connection.execute(
            "SELECT id, created_at, question, response_json FROM beacon_turns WHERE conversation_id = ? ORDER BY created_at",
            (conversation_id,),
        ).fetchall()
    return {
        **dict(conversation),
        "turns": [
            {
                "id": row["id"],
                "created_at": row["created_at"],
                "question": row["question"],
                "answer": json.loads(row["response_json"]),
            }
            for row in turns
        ],
    }
