"""CSV validation, canonical preparation, and deterministic snapshot generation."""

from __future__ import annotations

import csv
import io
from collections import Counter
from dataclasses import asdict
from datetime import date
from typing import Any
from uuid import uuid4

from app.services.analysis import Signal, build_snapshot, classify_signal


REQUIRED_COLUMNS = {
    "attendance": {"student_id", "class_name", "date", "status"},
    "behaviour": {"student_id", "class_name", "date", "incident_type", "severity"},
    "assessments": {"student_id", "class_name", "subject", "date", "score"},
}
VALID_ATTENDANCE = {"present", "absent", "late", "excused"}
VALID_SEVERITY = {"low", "medium", "high"}


class ImportValidationError(Exception):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


def parse_date(value: str, kind: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ImportValidationError(f"{kind.title()} contains an invalid ISO date: {value}.") from error


def parse_csv(content: bytes, kind: str) -> list[dict[str, Any]]:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ImportValidationError(f"{kind.title()} must be UTF-8 encoded.") from error
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ImportValidationError(f"{kind.title()} CSV is missing a header row.")
    columns = {column.strip() for column in reader.fieldnames if column}
    missing = sorted(REQUIRED_COLUMNS[kind] - columns)
    if missing:
        raise ImportValidationError(f"{kind.title()} CSV is missing required columns.", {"missing_columns": missing})
    rows: list[dict[str, Any]] = []
    for row_number, original in enumerate(reader, start=2):
        row = {key.strip(): (value or "").strip() for key, value in original.items() if key}
        if any(not row.get(field) for field in REQUIRED_COLUMNS[kind]):
            raise ImportValidationError(f"{kind.title()} row {row_number} contains an empty required value.")
        parse_date(row["date"], kind)
        if kind == "attendance" and row["status"].lower() not in VALID_ATTENDANCE:
            raise ImportValidationError(f"Attendance row {row_number} has an unsupported status: {row['status']}.")
        if kind == "behaviour" and row["severity"].lower() not in VALID_SEVERITY:
            raise ImportValidationError(f"Behaviour row {row_number} has an unsupported severity: {row['severity']}.")
        if kind == "assessments":
            try:
                score = float(row["score"])
            except ValueError as error:
                raise ImportValidationError(f"Assessments row {row_number} has a non-numeric score.") from error
            if not 0 <= score <= 100:
                raise ImportValidationError(f"Assessments row {row_number} has a score outside 0–100.")
            row["score"] = score
        row["kind"] = kind
        rows.append(row)
    if not rows:
        raise ImportValidationError(f"{kind.title()} CSV has no data rows.")
    return rows


def split_period(rows: list[dict[str, Any]], kind: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    dates = sorted({parse_date(str(row["date"]), kind) for row in rows})
    midpoint = len(dates) // 2
    if midpoint == 0:
        raise ImportValidationError(f"{kind.title()} needs records from at least two reporting dates.")
    previous_dates = set(dates[:midpoint])
    return (
        [row for row in rows if parse_date(str(row["date"]), kind) in previous_dates],
        [row for row in rows if parse_date(str(row["date"]), kind) not in previous_dates],
    )


def percentage_present(rows: list[dict[str, Any]]) -> float:
    return round(100 * sum(str(row["status"]).lower() in {"present", "late"} for row in rows) / len(rows), 1)


def average_score(rows: list[dict[str, Any]]) -> float:
    return round(sum(float(row["score"]) for row in rows) / len(rows), 1)


def make_signals(
    attendance: list[dict[str, Any]], behaviour: list[dict[str, Any]], assessments: list[dict[str, Any]], scope: str
) -> tuple[list[Signal], int]:
    previous_attendance, current_attendance = split_period(attendance, "attendance")
    previous_behaviour, current_behaviour = split_period(behaviour, "behaviour")
    mathematics = [row for row in assessments if str(row["subject"]).lower() in {"math", "maths", "mathematics"}] or assessments
    previous_assessment, current_assessment = split_period(mathematics, "assessments")
    values = {
        "attendance": (percentage_present(previous_attendance), percentage_present(current_attendance)),
        "behaviour": (len(previous_behaviour), len(current_behaviour)),
        "assessment": (average_score(previous_assessment), average_score(current_assessment)),
    }
    labels = {"attendance": "Attendance", "behaviour": "Behaviour incidents", "assessment": "Mathematics average"}
    signals: list[Signal] = []
    for category, (previous, current) in values.items():
        change = round(current - previous, 1)
        unit = "" if category == "behaviour" else "%"
        verb = "increased" if change > 0 else "declined" if change < 0 else "remained stable"
        fact = f"{labels[category]} {verb} from {previous}{unit} to {current}{unit}."
        signals.append(Signal(f"{category}_{scope}", category, fact, previous, current, change, classify_signal(category, change)))
    repeated = Counter(str(row["student_id"]) for row in current_attendance if str(row["status"]).lower() == "absent")
    return signals, sum(count > 1 for count in repeated.values())


def learner_summaries(rows: dict[str, list[dict[str, Any]]], class_name: str) -> list[dict[str, Any]]:
    learners = sorted({str(row["student_id"]) for dataset in rows.values() for row in dataset if row["class_name"] == class_name})
    summaries: list[dict[str, Any]] = []
    split = {kind: split_period([row for row in dataset if row["class_name"] == class_name], kind) for kind, dataset in rows.items()}
    for learner in learners:
        learner_name = next((str(row.get("first_name")) for dataset in rows.values() for row in dataset if row["student_id"] == learner and row.get("first_name")), learner)
        attendance_previous = [row for row in split["attendance"][0] if row["student_id"] == learner]
        attendance_current = [row for row in split["attendance"][1] if row["student_id"] == learner]
        behaviour_previous = [row for row in split["behaviour"][0] if row["student_id"] == learner]
        behaviour_current = [row for row in split["behaviour"][1] if row["student_id"] == learner]
        assessment_previous = [row for row in split["assessments"][0] if row["student_id"] == learner]
        assessment_current = [row for row in split["assessments"][1] if row["student_id"] == learner]
        previous_attendance = percentage_present(attendance_previous) if attendance_previous else None
        current_attendance = percentage_present(attendance_current) if attendance_current else None
        previous_score = average_score(assessment_previous) if assessment_previous else None
        current_score = average_score(assessment_current) if assessment_current else None
        factors: list[str] = []
        if previous_attendance is not None and current_attendance is not None and current_attendance < previous_attendance:
            factors.append("attendance_decline")
        if len(behaviour_current) > len(behaviour_previous):
            factors.append("behaviour_increase")
        if previous_score is not None and current_score is not None and current_score < previous_score:
            factors.append("assessment_decline")
        summaries.append({
            "student_id": learner, "learner_name": learner_name, "class_name": class_name,
            "attendance_previous": previous_attendance, "attendance_current": current_attendance,
            "behaviour_previous": len(behaviour_previous), "behaviour_current": len(behaviour_current),
            "assessment_previous": previous_score, "assessment_current": current_score,
            "risk_factors": factors,
        })
    return summaries


def subject_summaries(assessments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    keys = sorted({(str(row["class_name"]), str(row["subject"])) for row in assessments})
    for class_name, subject in keys:
        scoped = [row for row in assessments if row["class_name"] == class_name and row["subject"] == subject]
        try:
            previous, current = split_period(scoped, "assessments")
        except ImportValidationError:
            continue
        previous_value, current_value = average_score(previous), average_score(current)
        summaries.append({"class_name": class_name, "subject": subject, "previous_value": previous_value, "current_value": current_value, "change": round(current_value - previous_value, 1)})
    return summaries


def process_imports(
    attendance_content: bytes, behaviour_content: bytes, assessments_content: bytes, school_name: str = "Mufakose High"
) -> tuple[dict[str, Any], list[dict[str, Any]], str]:
    rows = {
        "attendance": parse_csv(attendance_content, "attendance"),
        "behaviour": parse_csv(behaviour_content, "behaviour"),
        "assessments": parse_csv(assessments_content, "assessments"),
    }
    shared_classes = set(row["class_name"] for row in rows["attendance"])
    shared_classes &= {row["class_name"] for row in rows["behaviour"]}
    shared_classes &= {row["class_name"] for row in rows["assessments"]}
    if not shared_classes:
        raise ImportValidationError("The three CSVs do not contain a shared class_name.")
    class_summaries: list[dict[str, Any]] = []
    all_learners: list[dict[str, Any]] = []
    for class_name in sorted(shared_classes):
        scoped = {kind: [row for row in dataset if row["class_name"] == class_name] for kind, dataset in rows.items()}
        signals, repeated_absences = make_signals(scoped["attendance"], scoped["behaviour"], scoped["assessments"], class_name.lower().replace(" ", "_"))
        risk_score = sum(3 if signal.severity == "high" else 1 if signal.severity == "medium" else 0 for signal in signals)
        class_summaries.append({"class_name": class_name, "risk_score": risk_score, "repeated_absences": repeated_absences, "signals": [asdict(signal) for signal in signals]})
        all_learners.extend(learner_summaries(rows, class_name))
    school_signals, _ = make_signals(rows["attendance"], rows["behaviour"], rows["assessments"], "school")
    import_id = f"import_{uuid4().hex}"
    analysis_id = f"analysis_{uuid4().hex}"
    trace_id = f"trace_{uuid4().hex}"
    canonical_records = [row for dataset in rows.values() for row in dataset]
    snapshot = build_snapshot(
        analysis_id=analysis_id, trace_id=trace_id, school_name=school_name,
        analysis_period="Uploaded reporting periods", class_summaries=class_summaries,
        school_signals=school_signals, learner_summaries=all_learners,
        subject_summaries=subject_summaries(rows["assessments"]),
        data_summary={
            "learners": len({row["student_id"] for row in canonical_records}),
            "classes": len(shared_classes),
            "attendance_records": len(rows["attendance"]),
            "behaviour_records": len(rows["behaviour"]),
            "assessment_records": len(rows["assessments"]),
        },
    )
    return snapshot, canonical_records, import_id


def build_evidence_from_imports(attendance_content: bytes, behaviour_content: bytes, assessments_content: bytes) -> dict[str, Any]:
    return process_imports(attendance_content, behaviour_content, assessments_content)[0]
