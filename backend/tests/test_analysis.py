import unittest

from app.services.analysis import build_demo_evidence, calculate_change, classify_signal


class AnalysisTests(unittest.TestCase):
    def test_calculates_verified_changes(self) -> None:
        self.assertEqual(calculate_change(92, 84), -8)
        self.assertEqual(calculate_change(2, 9), 7)

    def test_detects_grade_7a_high_signals(self) -> None:
        self.assertEqual(classify_signal("attendance", -8), "high")
        self.assertEqual(classify_signal("behaviour", 7), "high")
        self.assertEqual(classify_signal("assessment", -7), "high")

    def test_healthy_movement_is_not_presented_as_a_risk(self) -> None:
        self.assertEqual(classify_signal("attendance", 3), "healthy")
        self.assertEqual(classify_signal("behaviour", -2), "healthy")
        self.assertEqual(classify_signal("assessment", 4), "healthy")

    def test_evidence_package_is_traceable_and_balanced(self) -> None:
        evidence = build_demo_evidence()
        self.assertEqual(evidence["confidence"], 87)
        self.assertEqual(len(evidence["signals"]), 3)
        self.assertEqual(evidence["missing_evidence"], ["Learner-level records are not included in the prepared example."])
        self.assertEqual(len(evidence["school_metrics"]), 4)
        self.assertEqual(evidence["intervention"]["class_name"], evidence["class_name"])
        self.assertTrue(evidence["trace_id"])


if __name__ == "__main__":
    unittest.main()
