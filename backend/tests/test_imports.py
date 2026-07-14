import io
import os
import tempfile
import unittest
from pathlib import Path

TEST_DATABASE = Path(tempfile.gettempdir()) / "veriq_mvp_test.db"
os.environ["VERIQ_DB_PATH"] = str(TEST_DATABASE)
TEST_DATABASE.unlink(missing_ok=True)

from fastapi.testclient import TestClient

from app.main import app
from app.services.database import connect
from app.services.imports import ImportValidationError, build_evidence_from_imports


ATTENDANCE = """student_id,class_name,date,status
1,Grade 7A,2026-06-01,present
2,Grade 7A,2026-06-02,present
1,Grade 7A,2026-07-01,absent
2,Grade 7A,2026-07-02,absent
"""
BEHAVIOUR = """student_id,class_name,date,incident_type,severity
1,Grade 7A,2026-06-01,disruption,low
2,Grade 7A,2026-06-02,late,low
1,Grade 7A,2026-07-01,disruption,medium
2,Grade 7A,2026-07-02,disruption,medium
3,Grade 7A,2026-07-03,late,low
4,Grade 7A,2026-07-04,disruption,high
"""
ASSESSMENTS = """student_id,class_name,subject,date,score
1,Grade 7A,Mathematics,2026-06-01,80
2,Grade 7A,Mathematics,2026-06-02,76
1,Grade 7A,Mathematics,2026-07-01,65
2,Grade 7A,Mathematics,2026-07-02,60
"""


class ImportTests(unittest.TestCase):
    def test_csv_import_creates_traceable_evidence(self) -> None:
        evidence = build_evidence_from_imports(
            ATTENDANCE.encode(), BEHAVIOUR.encode(), ASSESSMENTS.encode()
        )
        self.assertEqual(evidence["class_name"], "Grade 7A")
        self.assertEqual(len(evidence["signals"]), 3)
        self.assertTrue(evidence["trace_id"].startswith("trace_"))
        self.assertTrue(evidence["analysis_id"].startswith("analysis_"))
        self.assertIn("Attendance declined from 100.0% to 0.0%.", evidence["supporting_evidence"])
        self.assertEqual(evidence["data_summary"]["learners"], 4)

    def test_missing_required_column_is_rejected(self) -> None:
        with self.assertRaises(ImportValidationError):
            build_evidence_from_imports(
                b"student_id,class_name,date\n1,Grade 7A,2026-06-01\n",
                BEHAVIOUR.encode(),
                ASSESSMENTS.encode(),
            )

    def test_import_endpoint_updates_latest_evidence(self) -> None:
        files = {
            "attendance": ("attendance.csv", io.BytesIO(ATTENDANCE.encode()), "text/csv"),
            "behaviour": ("behaviour.csv", io.BytesIO(BEHAVIOUR.encode()), "text/csv"),
            "assessments": ("assessments.csv", io.BytesIO(ASSESSMENTS.encode()), "text/csv"),
        }
        client = TestClient(app)
        imported = client.post(
            "/api/v1/imports/analyse",
            files=files,
            data={"data_use_acknowledged": "true"},
        )
        latest = client.get("/api/v1/intelligence/latest-evidence")
        latest_decision = client.get("/api/v1/decisions/latest")
        self.assertEqual(imported.status_code, 201)
        self.assertEqual(imported.json()["metadata"]["source"], "csv_import")
        self.assertEqual(latest.json()["data"]["trace_id"], imported.json()["data"]["trace_id"])
        self.assertEqual(latest.json()["data"]["analysis_id"], imported.json()["data"]["analysis_id"])
        self.assertEqual(imported.json()["metadata"]["records_stored"], 14)
        self.assertTrue(imported.json()["metadata"]["data_use_acknowledged"])
        self.assertEqual(latest_decision.status_code, 200)
        self.assertIsNone(latest_decision.json()["data"])
        with connect() as database:
            stored_import = database.execute("SELECT length(attendance_csv) AS raw_size FROM imports ORDER BY created_at DESC LIMIT 1").fetchone()
            stored_records = database.execute("SELECT count(*) AS total FROM school_records").fetchone()
        self.assertGreater(stored_import["raw_size"], 0)
        self.assertEqual(stored_records["total"], 14)

    def test_invalid_domain_values_are_rejected(self) -> None:
        with self.assertRaises(ImportValidationError):
            build_evidence_from_imports(
                ATTENDANCE.replace("present", "unknown", 1).encode(),
                BEHAVIOUR.encode(), ASSESSMENTS.encode(),
            )
        with self.assertRaises(ImportValidationError):
            build_evidence_from_imports(
                ATTENDANCE.encode(), BEHAVIOUR.encode(),
                ASSESSMENTS.replace(",80", ",180", 1).encode(),
            )

    def test_workspace_identity_persists_and_is_used_by_new_imports(self) -> None:
        client = TestClient(app)
        workspace = {
            "school_name": "Connected Test School",
            "school_location": "Harare, Zimbabwe",
            "user_name": "Rudo Moyo",
            "user_role": "Deputy Head",
        }
        updated = client.patch("/api/v1/workspace", json=workspace)
        loaded = client.get("/api/v1/workspace")
        files = {
            "attendance": ("attendance.csv", io.BytesIO(ATTENDANCE.encode()), "text/csv"),
            "behaviour": ("behaviour.csv", io.BytesIO(BEHAVIOUR.encode()), "text/csv"),
            "assessments": ("assessments.csv", io.BytesIO(ASSESSMENTS.encode()), "text/csv"),
        }
        imported = client.post(
            "/api/v1/imports/analyse",
            files=files,
            data={"data_use_acknowledged": "true"},
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(loaded.json()["data"]["user_name"], "Rudo Moyo")
        self.assertEqual(imported.json()["data"]["school_name"], "Connected Test School")

    def test_import_endpoint_requires_data_use_acknowledgement(self) -> None:
        files = {
            "attendance": ("attendance.csv", io.BytesIO(ATTENDANCE.encode()), "text/csv"),
            "behaviour": ("behaviour.csv", io.BytesIO(BEHAVIOUR.encode()), "text/csv"),
            "assessments": ("assessments.csv", io.BytesIO(ASSESSMENTS.encode()), "text/csv"),
        }
        client = TestClient(app)
        response = client.post(
            "/api/v1/imports/analyse",
            files=files,
            data={"data_use_acknowledged": "false"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "VALIDATION_ERROR")
        self.assertIn("authorised", response.json()["error"]["message"])


if __name__ == "__main__":
    unittest.main()
