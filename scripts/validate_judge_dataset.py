"""Validate the committed judge dataset with the same evidence engine used by the API."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
DATASET = ROOT / "demo-data" / "zimbabwe-secondary-judge"
REPORT = ROOT / "submission" / "dataset" / "SYNTHETIC_VALIDATION_RESULTS.json"
sys.path.insert(0, str(BACKEND))

from app.services.imports import build_evidence_from_imports  # noqa: E402


def read_rows(name: str) -> list[dict[str, str]]:
    with (DATASET / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(name: str) -> str:
    return hashlib.sha256((DATASET / name).read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    attendance = read_rows("attendance.csv")
    behaviour = read_rows("behaviour.csv")
    assessments = read_rows("assessments.csv")
    evidence = build_evidence_from_imports(
        (DATASET / "attendance.csv").read_bytes(),
        (DATASET / "behaviour.csv").read_bytes(),
        (DATASET / "assessments.csv").read_bytes(),
    )

    require(len(attendance) == 400, "Attendance must contain 400 records.")
    require(len(behaviour) == 34, "Behaviour must contain 34 records.")
    require(len(assessments) == 400, "Assessments must contain 400 records.")
    require(evidence["data_summary"]["learners"] == 20, "Dataset must contain 20 learners.")
    require(evidence["data_summary"]["classes"] == 4, "Dataset must contain four shared classes.")

    classes = sorted({row["class_name"] for row in attendance})
    subjects = sorted({row["subject"] for row in assessments})
    require(classes == ["Form 1A", "Form 2A", "Form 3A", "Form 4A"], "Unexpected class set.")
    require(subjects == ["Combined Science", "English Language", "Heritage Studies", "Mathematics", "Shona Language"], "Unexpected subject set.")
    require(all(0 <= float(row["score"]) <= 100 for row in assessments), "Scores must remain in 0-100.")
    require(all(row["status"] in {"present", "absent", "late", "excused"} for row in attendance), "Unsupported attendance status.")
    require(all(row["severity"] in {"low", "medium", "high"} for row in behaviour), "Unsupported behaviour severity.")

    identity = {}
    for row in attendance + behaviour + assessments:
        current = (row.get("first_name", ""), row["class_name"])
        require(row["student_id"] not in identity or identity[row["student_id"]] == current, "A learner ID maps to multiple identities.")
        identity[row["student_id"]] = current
    require(len(identity) == 20, "Learner identifiers are not one-to-one.")

    require(len({(row["student_id"], row["date"]) for row in attendance}) == len(attendance), "Duplicate attendance key.")
    require(len({(row["student_id"], row["subject"], row["date"]) for row in assessments}) == len(assessments), "Duplicate assessment key.")
    require(len({(row["student_id"], row["date"], row["incident_type"]) for row in behaviour}) == len(behaviour), "Duplicate behaviour key.")

    learners = {item["learner_name"]: item for item in evidence["learner_summaries"]}
    triple = {name for name, item in learners.items() if set(item["risk_factors"]) == {"attendance_decline", "behaviour_increase", "assessment_decline"}}
    watch = {name for name, item in learners.items() if item["risk_factors"] and name not in triple}
    stable = {name for name, item in learners.items() if not item["risk_factors"]}
    require(triple == {"Chipo", "Tendai", "Nyasha"}, f"Connected high-attention set is wrong: {sorted(triple)}")
    require(watch == {"Tapiwa", "Tanaka"}, f"Watch set is wrong: {sorted(watch)}")
    require(len(stable) == 15, "Exactly fifteen controls must remain stable or improving.")

    no_official_outcome_fields = {"zimsec_grade", "pass_rate", "final_result"}.isdisjoint(assessments[0].keys())
    require(no_official_outcome_fields, "Dataset must not imply official final outcomes.")

    report = {
        "validation_status": "passed",
        "validation_date": "2026-07-14",
        "validated_with": "backend/app/services/imports.py",
        "data_summary": evidence["data_summary"],
        "classes": classes,
        "subjects": subjects,
        "periods": {
            "attendance_dates": [min(row["date"] for row in attendance), max(row["date"] for row in attendance)],
            "assessment_dates": [min(row["date"] for row in assessments), max(row["date"] for row in assessments)],
        },
        "scenario_results": {
            "connected_high_attention": {name: learners[name] for name in sorted(triple)},
            "single_signal_watch": {name: learners[name] for name in sorted(watch)},
            "stable_control_count": len(stable),
        },
        "class_results": [
            {
                "class_name": item["class_name"],
                "risk_score": item["risk_score"],
                "repeated_absences": item["repeated_absences"],
                "signals": item["signals"],
            }
            for item in evidence["class_summaries"]
        ],
        "integrity_checks": {
            "unique_learner_ids": len(identity),
            "duplicate_attendance_keys": 0,
            "duplicate_behaviour_keys": 0,
            "duplicate_assessment_keys": 0,
            "scores_in_range": True,
            "valid_domain_values": True,
            "official_outcome_claims_present": False,
        },
        "sha256": {
            "attendance.csv": sha256("attendance.csv"),
            "behaviour.csv": sha256("behaviour.csv"),
            "assessments.csv": sha256("assessments.csv"),
        },
        "behaviour_severity_distribution": dict(sorted(Counter(row["severity"] for row in behaviour).items())),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: wrote {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
