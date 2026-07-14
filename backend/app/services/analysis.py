"""Deterministic educational calculations and intelligence snapshot contracts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any


ATTENDANCE_HIGH_DECLINE = -8
BEHAVIOUR_HIGH_INCREASE = 6
ASSESSMENT_HIGH_DECLINE = -7
DEMO_CONFIDENCE = 87


@dataclass(frozen=True)
class Signal:
    id: str
    category: str
    fact: str
    previous_value: int | float
    current_value: int | float
    change: int | float
    severity: str


def calculate_change(previous_value: int | float, current_value: int | float) -> int | float:
    return current_value - previous_value


def classify_signal(category: str, change: int | float) -> str:
    """Separates concerning, watch, and healthy movements."""
    if category == "behaviour":
        if change >= BEHAVIOUR_HIGH_INCREASE:
            return "high"
        return "medium" if change > 0 else "healthy"
    threshold = ATTENDANCE_HIGH_DECLINE if category == "attendance" else ASSESSMENT_HIGH_DECLINE
    if change <= threshold:
        return "high"
    return "medium" if change < 0 else "healthy"


def signal_tone(signal: Signal) -> str:
    return "positive" if signal.severity == "healthy" else "attention"


def recommended_actions(signals: list[Signal], class_name: str, repeated_absences: int = 0) -> list[str]:
    categories = {signal.category for signal in signals if signal.severity != "healthy"}
    actions: list[str] = []
    if "attendance" in categories:
        detail = f"Review the {repeated_absences} learners with repeated absences" if repeated_absences else "Review recent absence records"
        actions.append(f"{detail} with the attendance lead.")
    if "behaviour" in categories:
        actions.append(f"Meet the {class_name} class teacher to review behaviour context.")
    if "assessment" in categories:
        actions.append("Agree targeted Mathematics support before the next assessment review.")
    if not actions:
        actions.append("Continue monitoring the current pattern as new evidence arrives.")
    return actions


def build_snapshot(
    *,
    analysis_id: str,
    trace_id: str,
    school_name: str,
    analysis_period: str,
    class_summaries: list[dict[str, Any]],
    school_signals: list[Signal],
    learner_summaries: list[dict[str, Any]],
    subject_summaries: list[dict[str, Any]],
    data_summary: dict[str, int],
    missing_evidence: list[str] | None = None,
    confidence: int | None = None,
) -> dict[str, Any]:
    ranked = sorted(class_summaries, key=lambda item: (-item["risk_score"], item["class_name"]))
    primary = ranked[0]
    signals = [Signal(**signal) if isinstance(signal, dict) else signal for signal in primary["signals"]]
    high_signals = sum(signal.severity == "high" for signal in signals)
    calculated_confidence = min(92, 68 + high_signals * 8 + len(signals) * 3)
    confidence = confidence or calculated_confidence
    gaps = missing_evidence or []
    actions = recommended_actions(signals, primary["class_name"], primary.get("repeated_absences", 0))
    concerning = [signal for signal in signals if signal.severity != "healthy"]
    pattern = concerning or signals
    categories = [signal.category for signal in pattern]
    title_categories = ["Mathematics" if category == "assessment" else category.title() for category in categories]
    title = " and ".join(title_categories[:2]) + " early intervention" if concerning else f"Sustain {primary['class_name']} progress"
    summary = " ".join(signal.fact for signal in pattern)
    priorities = [
        {
            "id": f"priority_{item['class_name'].lower().replace(' ', '_')}",
            "class_name": item["class_name"],
            "level": "High" if item["risk_score"] >= 6 else "Medium" if item["risk_score"] else "Watch",
            "title": f"{item['class_name']} needs an early evidence review" if item["risk_score"] else f"{item['class_name']} is stable",
            "description": " ".join(signal["fact"] for signal in item["signals"] if signal["severity"] != "healthy") or "The latest indicators are stable or improving.",
            "scope_id": item["class_name"],
        }
        for item in ranked[:3]
    ]
    school_metrics = [
        {
            "id": signal.category,
            "category": signal.category,
            "label": "Assessment" if signal.category == "assessment" else signal.category.title(),
            "previous_value": signal.previous_value,
            "current_value": signal.current_value,
            "change": signal.change,
            "unit": "incidents" if signal.category == "behaviour" else "%",
            "tone": signal_tone(signal),
            "fact": signal.fact,
        }
        for signal in school_signals
    ]
    overall_status = "Needs attention" if any(signal.severity == "high" for signal in signals) else "Stable"
    school_metrics.append(
        {
            "id": "school-health", "category": "school_health", "label": "School health",
            "previous_value": 0, "current_value": 0, "change": 0, "unit": "status",
            "tone": "attention" if overall_status == "Needs attention" else "positive",
            "fact": f"{primary['class_name']} is the highest-priority class in the current evidence.",
            "display_value": overall_status,
        }
    )
    return {
        "analysis_id": analysis_id,
        "school_name": school_name,
        "class_name": primary["class_name"],
        "analysis_period": analysis_period,
        "generated_at": datetime.now(UTC).isoformat(),
        "signals": [asdict(signal) for signal in signals],
        "school_metrics": school_metrics,
        "class_summaries": ranked,
        "learner_summaries": learner_summaries,
        "subject_summaries": subject_summaries,
        "priorities": priorities,
        "alerts": [
            {"id": f"alert_{signal.id}", "category": signal.category, "title": f"{signal.category.title()} evidence updated", "detail": signal.fact, "tone": signal_tone(signal)}
            for signal in school_signals
        ],
        "intervention": {
            "class_name": primary["class_name"], "title": title,
            "summary": summary, "priority": priorities[0]["level"], "actions": actions,
        },
        "supporting_evidence": [signal.fact for signal in signals] + ([f"{primary['repeated_absences']} learners have repeated absences in the current period."] if primary.get("repeated_absences") else []),
        "contradicting_evidence": [],
        "missing_evidence": gaps,
        "confidence": confidence,
        "confidence_explanation": f"Confidence is based on three validated data sources across {data_summary['classes']} class{'es' if data_summary['classes'] != 1 else ''}; it reflects consistency, completeness and signal strength.",
        "allowed_recommendation_categories": ["teacher_meeting", "attendance_review", "parent_engagement", "mathematics_support", "continued_monitoring"],
        "data_summary": data_summary,
        "trace_id": trace_id,
    }


def build_demo_evidence() -> dict[str, Any]:
    """One internally consistent prepared snapshot shown before the first upload."""
    signals = [
        Signal("attendance_grade_7a", "attendance", "Attendance declined from 92% to 84%.", 92, 84, -8, "high"),
        Signal("behaviour_grade_7a", "behaviour", "Behaviour incidents increased from 2 to 9.", 2, 9, 7, "high"),
        Signal("mathematics_grade_7a", "assessment", "Mathematics average declined from 68% to 61%.", 68, 61, -7, "high"),
    ]
    return build_snapshot(
        analysis_id="analysis_prepared_001", trace_id="trace_prepared_grade_7a_001",
        school_name="Mufakose High", analysis_period="Prepared four-week example",
        class_summaries=[{"class_name": "Grade 7A", "risk_score": 9, "repeated_absences": 8, "signals": [asdict(signal) for signal in signals]}],
        school_signals=signals, learner_summaries=[],
        subject_summaries=[{"class_name": "Grade 7A", "subject": "Mathematics", "previous_value": 68, "current_value": 61, "change": -7}],
        data_summary={"learners": 0, "classes": 1, "attendance_records": 0, "behaviour_records": 0, "assessment_records": 0},
        missing_evidence=["Learner-level records are not included in the prepared example."], confidence=DEMO_CONFIDENCE,
    )
