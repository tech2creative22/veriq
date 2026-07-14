"""Persistent Evidence Snapshot access for the single-school MVP."""

from typing import Any

from app.services.analysis import build_demo_evidence
from app.services.database import latest_snapshot, save_snapshot


def set_latest_evidence(evidence: dict[str, Any], source: str = "csv_import", import_id: str | None = None) -> None:
    save_snapshot(evidence, source, import_id)


def get_latest_evidence() -> tuple[dict[str, Any], str]:
    stored = latest_snapshot()
    if stored is not None:
        return stored
    prepared = build_demo_evidence()
    save_snapshot(prepared, "prepared_example")
    return prepared, "prepared_example"
