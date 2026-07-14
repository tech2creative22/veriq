"""Run the deterministic grounding and scope evaluation suite and write JSON evidence."""

from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
TESTS = BACKEND / "tests"
REPORT = ROOT / "submission" / "ai" / "BEACON_TEST_RESULTS.json"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(TESTS))


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.records: list[dict[str, str]] = []

    def addSuccess(self, test: unittest.case.TestCase) -> None:
        super().addSuccess(test)
        self.records.append({"test": test.id(), "status": "passed"})

    def addFailure(self, test: unittest.case.TestCase, err: object) -> None:
        super().addFailure(test, err)
        self.records.append({"test": test.id(), "status": "failed"})

    def addError(self, test: unittest.case.TestCase, err: object) -> None:
        super().addError(test, err)
        self.records.append({"test": test.id(), "status": "error"})

    def addSkip(self, test: unittest.case.TestCase, reason: str) -> None:
        super().addSkip(test, reason)
        self.records.append({"test": test.id(), "status": "skipped", "reason": reason})


def main() -> None:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite([
        loader.loadTestsFromName("test_analysis"),
        loader.loadTestsFromName("test_beacon"),
    ])
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=2, resultclass=RecordingResult)
    result = runner.run(suite)
    report = {
        "evaluation_date": "2026-07-14",
        "evaluation_type": "deterministic evidence, scope, grounding and provider-boundary regression",
        "live_model_semantic_benchmark": False,
        "tests_run": result.testsRun,
        "passed": sum(record["status"] == "passed" for record in result.records),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "tests": sorted(result.records, key=lambda record: record["test"]),
        "interpretation": "These tests prove application controls and grounding invariants. They do not replace educator usability testing or repeated live-model quality evaluation.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{'PASS' if result.wasSuccessful() else 'FAIL'}: {report['passed']}/{result.testsRun} tests; wrote {REPORT.relative_to(ROOT)}")
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
