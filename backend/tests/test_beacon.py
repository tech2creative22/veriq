import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TEST_DATABASE = Path(tempfile.gettempdir()) / "veriq_mvp_test.db"
os.environ["VERIQ_DB_PATH"] = str(TEST_DATABASE)
TEST_DATABASE.unlink(missing_ok=True)

from fastapi.testclient import TestClient

from app.main import app
from app.services.analysis import build_demo_evidence
from app.services.beacon import (
    BeaconConfigurationError,
    BeaconGroundingError,
    explain_with_gemini,
    get_conversational_reply,
    get_scope_clarification,
    resolve_question_scope,
    scope_evidence,
)


def evidence_with_learners() -> dict:
    evidence = build_demo_evidence()
    evidence["learner_summaries"] = [
        {
            "student_id": "G7A-002", "learner_name": "Chipo", "class_name": "Grade 7A",
            "attendance_previous": 100.0, "attendance_current": 40.0,
            "behaviour_previous": 1, "behaviour_current": 4,
            "assessment_previous": 71.0, "assessment_current": 58.0,
            "risk_factors": ["attendance_decline", "behaviour_increase", "assessment_decline"],
        },
        {
            "student_id": "G7A-004", "learner_name": "Tariro", "class_name": "Grade 7A",
            "attendance_previous": 100.0, "attendance_current": 100.0,
            "behaviour_previous": 0, "behaviour_current": 0,
            "assessment_previous": 79.0, "assessment_current": 81.0,
            "risk_factors": [],
        },
    ]
    return evidence


def valid_completion(_prompt: str) -> str:
    return json.dumps(
        {
            "situation": "Grade 7A shows an early pattern across attendance, behaviour, and Mathematics.",
            "why_it_matters": "The combined changes suggest that a focused review may prevent the pattern from becoming more serious.",
            "supporting_evidence_ids": ["evidence_1", "evidence_2", "evidence_3"],
            "recommendation_category": "attendance_review",
            "recommendation": "A recommended next step is a brief attendance and classroom review with the relevant staff.",
            "suggested_next_step": "Confirm the repeated-absence learners for a supportive check-in this week.",
        }
    )


class BeaconTests(unittest.TestCase):
    def test_unknown_learner_is_intercepted_before_gemini(self) -> None:
        response = get_scope_clarification(
            "Give me performance for Rudo", evidence_with_learners()
        )
        self.assertIsNotNone(response)
        self.assertEqual(response["response_type"], "clarification")
        self.assertIn("Chipo", response["available_learners"])
        self.assertIn("Tariro", response["available_learners"])

    def test_known_learner_does_not_trigger_clarification(self) -> None:
        self.assertIsNone(
            get_scope_clarification("Give me performance for Chipo", evidence_with_learners())
        )

    def test_named_learner_overrides_broad_page_scope(self) -> None:
        scope = resolve_question_scope(
            "Give me performance for Chipo", evidence_with_learners(), "school", None
        )
        self.assertEqual(scope, ("learner", "G7A-002"))

    def test_learner_scope_replaces_class_signals_with_learner_records(self) -> None:
        evidence = evidence_with_learners()
        scoped = scope_evidence(evidence, "learner", "G7A-002")
        self.assertEqual(scoped["active_scope"]["name"], "Chipo")
        self.assertEqual(
            [(signal["previous_value"], signal["current_value"]) for signal in scoped["signals"]],
            [(100.0, 40.0), (1, 4), (71.0, 58.0)],
        )
        self.assertTrue(all("Chipo" in fact for fact in scoped["supporting_evidence"]))
        self.assertNotIn("95", " ".join(scoped["supporting_evidence"]))
        self.assertIn("learner-level", scoped["confidence_explanation"])

    def test_different_learners_receive_different_verified_signals(self) -> None:
        evidence = evidence_with_learners()
        chipo = scope_evidence(evidence, "learner", "Chipo")
        tariro = scope_evidence(evidence, "learner", "Tariro")
        self.assertNotEqual(chipo["supporting_evidence"], tariro["supporting_evidence"])
        self.assertTrue(all(signal["severity"] == "healthy" for signal in tariro["signals"]))
        self.assertIn("79.0% to 81.0%", tariro["supporting_evidence"][-1])
        self.assertEqual(tariro["allowed_recommendation_categories"], ["continued_monitoring"])
        self.assertIn("parent_engagement", chipo["allowed_recommendation_categories"])

    def test_unknown_learner_name_keeps_requested_scope(self) -> None:
        scope = resolve_question_scope(
            "Give me performance for Rudo", evidence_with_learners(), "school", None
        )
        self.assertEqual(scope, ("school", None))

    def test_greeting_gets_a_brief_conversational_reply(self) -> None:
        evidence = build_demo_evidence()
        response = get_conversational_reply("hello", evidence)
        self.assertIsNotNone(response)
        self.assertEqual(response["response_type"], "conversation")
        self.assertIn(evidence["class_name"], response["message"])

    def test_evidence_question_is_not_intercepted_as_small_talk(self) -> None:
        response = get_conversational_reply(
            "Hello, why is Grade 7A at risk?", build_demo_evidence()
        )
        self.assertIsNone(response)

    def test_metric_scope_prioritises_the_selected_verified_metric(self) -> None:
        evidence = build_demo_evidence()
        attendance_metric = next(item for item in evidence["school_metrics"] if item["id"] == "attendance")
        attendance_metric.update({"previous_value": 94, "current_value": 91, "change": -3, "fact": "School attendance changed from 94% to 91%."})
        scoped = scope_evidence(evidence, "metric", "attendance")
        self.assertEqual(scoped["signals"][0]["category"], "attendance")
        self.assertEqual(scoped["signals"][0]["current_value"], 91)
        self.assertIn("School attendance", scoped["supporting_evidence"][0])

    def test_school_scope_uses_school_aggregates_not_primary_class_signals(self) -> None:
        evidence = build_demo_evidence()
        attendance_metric = next(item for item in evidence["school_metrics"] if item["id"] == "attendance")
        attendance_metric.update({"previous_value": 94, "current_value": 91, "change": -3, "fact": "School attendance changed from 94% to 91%."})
        scoped = scope_evidence(evidence, "school", None)
        self.assertEqual(scoped["signals"][0]["current_value"], 91)
        self.assertNotEqual(scoped["signals"][0]["current_value"], evidence["signals"][0]["current_value"])

    def test_greeting_endpoint_does_not_call_gemini(self) -> None:
        with patch("app.main.explain_with_gemini") as provider:
            response = TestClient(app).post(
                "/api/v1/beacon/explain", json={"question": "hello"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["response_type"], "conversation")
        provider.assert_not_called()

    def test_response_reuses_verified_confidence_and_evidence(self) -> None:
        evidence = build_demo_evidence()
        response = explain_with_gemini(
            "Why is Grade 7A being flagged?", evidence, valid_completion
        )
        self.assertEqual(response["confidence"], evidence["confidence"])
        self.assertEqual(
            response["supporting_evidence"], evidence["supporting_evidence"][:3]
        )
        self.assertEqual(response["missing_evidence"], evidence["missing_evidence"])
        self.assertEqual(response["trace_id"], evidence["trace_id"])

    def test_exam_readiness_question_compares_classes_without_claiming_official_pass_rate(self) -> None:
        evidence = build_demo_evidence()
        evidence["school_name"] = "Prince High"
        evidence["class_summaries"] = [
            {
                "class_name": "Form 4A", "risk_score": 7, "repeated_absences": 1,
                "signals": [
                    {"id": "attendance_form_4a", "category": "attendance", "fact": "Attendance declined from 96% to 88%.", "previous_value": 96, "current_value": 88, "change": -8, "severity": "high"},
                    {"id": "behaviour_form_4a", "category": "behaviour", "fact": "Behaviour incidents increased from 2 to 10.", "previous_value": 2, "current_value": 10, "change": 8, "severity": "high"},
                ],
            },
            {"class_name": "Form 3A", "risk_score": 1, "repeated_absences": 0, "signals": []},
        ]
        evidence["subject_summaries"] = [
            {"class_name": "Form 4A", "subject": "Mathematics", "previous_value": 65, "current_value": 58, "change": -7},
            {"class_name": "Form 4A", "subject": "English Language", "previous_value": 67, "current_value": 60, "change": -7},
            {"class_name": "Form 3A", "subject": "Mathematics", "previous_value": 70, "current_value": 72, "change": 2},
            {"class_name": "Form 3A", "subject": "English Language", "previous_value": 72, "current_value": 74, "change": 2},
        ]
        scoped = scope_evidence(evidence, "school", None)
        response = explain_with_gemini(
            "Which Form is least ready for O-Level, and can you claim an official pass rate?",
            scoped,
            valid_completion,
        )
        self.assertIn("Form 4A", response["situation"])
        self.assertIn("59.0%", response["situation"])
        self.assertIn("cannot claim an official O-Level pass rate", response["why_it_matters"])
        self.assertIn("internal assessment average", response["supporting_evidence"][0])
        self.assertIn("final ZIMSEC subject grades", response["missing_evidence"][-1])

    def test_unverified_evidence_is_rejected(self) -> None:
        def unsafe_completion(_prompt: str) -> str:
            payload = json.loads(valid_completion(""))
            payload["supporting_evidence_ids"] = ["evidence_999"]
            return json.dumps(payload)

        with self.assertRaises(BeaconGroundingError):
            explain_with_gemini("What evidence supports this?", build_demo_evidence(), unsafe_completion)

    def test_unverified_number_in_draft_is_not_exposed(self) -> None:
        def unsafe_completion(_prompt: str) -> str:
            payload = json.loads(valid_completion(""))
            payload["recommendation"] = "We recommend meeting 27 additional learners this week."
            return json.dumps(payload)

        response = explain_with_gemini(
            "What evidence supports this?", build_demo_evidence(), unsafe_completion
        )
        self.assertNotIn("27", response["recommendation"])

    def test_conversation_is_persisted_and_can_be_reopened(self) -> None:
        client = TestClient(app)
        created = client.post("/api/v1/beacon/explain", json={"question": "hello"})
        conversation_id = created.json()["data"]["conversation_id"]
        conversations = client.get("/api/v1/beacon/conversations")
        reopened = client.get(f"/api/v1/beacon/conversations/{conversation_id}")
        self.assertEqual(conversations.status_code, 200)
        self.assertEqual(reopened.status_code, 200)
        self.assertEqual(reopened.json()["data"]["turns"][0]["question"], "hello")

    def test_missing_key_is_reported_before_a_live_request(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(BeaconConfigurationError):
                explain_with_gemini("What evidence supports this?", build_demo_evidence())

    def test_configured_key_uses_the_gemini_provider(self) -> None:
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=True):
            with patch(
                "app.services.beacon.request_gemini_completion",
                return_value=valid_completion(""),
            ) as provider:
                explain_with_gemini("What evidence supports this?", build_demo_evidence())
        provider.assert_called_once()

    def test_endpoint_returns_a_safe_configuration_error_without_key(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            response = TestClient(app).post(
                "/api/v1/beacon/explain",
                json={"question": "Why is Grade 7A being flagged?"},
            )
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["error"]["code"], "GEMINI_NOT_CONFIGURED")


if __name__ == "__main__":
    unittest.main()
