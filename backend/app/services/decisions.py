"""Creates small, persistent Decision Objects from verified intelligence."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any
from uuid import uuid4

from app.services.database import save_decision


def create_decision(evidence: dict[str, Any], explanation: dict[str, Any], owner: str = "Deputy Head") -> dict[str, Any]:
    signals = evidence["signals"]
    attendance = next((signal for signal in signals if signal["category"] == "attendance"), None)
    behaviour = next((signal for signal in signals if signal["category"] == "behaviour"), None)
    assessment = next((signal for signal in signals if signal["category"] == "assessment"), None)
    targets: list[dict[str, str]] = []
    if attendance:
        targets.append({"label": "Attendance", "current": f"{attendance['current_value']}%", "target": f"{min(100, max(90, attendance['current_value'] + 5))}%", "note": "response target within four weeks"})
    if behaviour:
        targets.append({"label": "Behaviour", "current": f"{behaviour['current_value']} incidents", "target": f"{max(0, behaviour['current_value'] - max(1, round(behaviour['current_value'] * .25)))} incidents", "note": "response target within four weeks"})
    if assessment:
        targets.append({"label": "Mathematics", "current": f"{assessment['current_value']}%", "target": f"{min(100, assessment['current_value'] + 5)}%", "note": "response target by the next assessment review"})
    today = date.today()
    active_scope = evidence.get("active_scope", {"type": "class", "id": evidence["class_name"], "name": evidence["class_name"]})
    decision = {
        "id": f"decision_{uuid4().hex}",
        "analysis_id": evidence["analysis_id"],
        "trace_id": evidence["trace_id"],
        "class_name": evidence["class_name"],
        "scope_type": active_scope.get("type", "class"),
        "scope_id": active_scope.get("id"),
        "scope_label": active_scope.get("name") or evidence["class_name"],
        "title": evidence["intervention"]["title"],
        "situation": explanation["situation"],
        "why_it_matters": explanation["why_it_matters"],
        "recommendation": explanation["recommendation"],
        "evidence_summary": explanation["supporting_evidence"],
        "confidence": evidence["confidence"],
        "missing_evidence": evidence["missing_evidence"],
        "priority": evidence["intervention"]["priority"],
        "owner": owner,
        "due_date": (today + timedelta(days=7)).isoformat(),
        "review_date": (today + timedelta(days=14)).isoformat(),
        "status": "draft",
        "success_metric": targets[0]["target"] if targets else "Review the next evidence upload",
        "expected_outcomes": targets,
        "actions": evidence["intervention"]["actions"],
    }
    save_decision(decision)
    return decision
