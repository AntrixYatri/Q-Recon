import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.data_integration.unified_data_builder import build_canonical_record
from ai_engine.discrepancy_engine.discrepancy_detector import detect_discrepancies
from ai_engine.data_integration.record_linker import group_records

class TestMissingFieldHardening(unittest.TestCase):
    def test_missing_required_field_alert(self):
        # QCR has measured_value
        rec_qcr = build_canonical_record("doc-1", "QCR", {
            "project_code": "PRJ-103",
            "measured_value": "150 mm",
            "required_value": "150 mm",
            "unit": "mm",
            "parameter": "Pavement Thickness"
        })
        
        # Test Datasheet missing measured_value
        rec_td = build_canonical_record("doc-2", "TEST_DATASHEET", {
            "project_code": "PRJ-103",
            "required_value": "150 mm",
            "unit": "mm",
            "parameter": "Pavement Thickness"
        })
        
        discs = detect_discrepancies([rec_qcr, rec_td])
        
        # We expect a missing_value discrepancy on measured_value
        missing_disc = [d for d in discs if d["field"] == "measured_value" and d["discrepancy_type"] == "missing_value"]
        self.assertEqual(len(missing_disc), 1)

    def test_missing_optional_field_no_alert(self):
        # state is optional (check_missing is False)
        rec_qcr = build_canonical_record("doc-1", "QCR", {
            "project_code": "PRJ-103",
            "state": "Karnataka"
        })
        rec_td = build_canonical_record("doc-2", "TEST_DATASHEET", {
            "project_code": "PRJ-103"
        })
        
        discs = detect_discrepancies([rec_qcr, rec_td])
        
        # No missing_value discrepancy on state
        state_disc = [d for d in discs if d["field"] == "state" and d["discrepancy_type"] == "missing_value"]
        self.assertEqual(len(state_disc), 0)

    def test_missing_identity_prevents_unsafe_linking(self):
        # If project_code and road_name are both missing/empty, they should not group together
        rec_a = build_canonical_record("doc-1", "QCR", {})
        rec_b = build_canonical_record("doc-2", "TEST_DATASHEET", {})
        
        groups = group_records([rec_a, rec_b])
        # They should be placed in separate groups or isolated, not linked together
        self.assertGreaterEqual(len(groups), 2)

if __name__ == "__main__":
    unittest.main()
