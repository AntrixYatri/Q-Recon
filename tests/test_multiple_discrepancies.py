import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.data_integration.unified_data_builder import build_canonical_record
from ai_engine.discrepancy_engine.discrepancy_detector import detect_discrepancies

class TestMultipleDiscrepancies(unittest.TestCase):
    def test_independent_multiple_discrepancies(self):
        # QCR
        rec_qcr = build_canonical_record("qcr-doc", "QCR", {
            "project_code": "PRJ-101",
            "measured_value": "150 mm",
            "required_value": "150 mm",
            "unit": "mm",
            "quality_status": "compliant",
            "inspection_date": "2026-03-04"
        })
        
        # Test Datasheet: measured_value is 120 mm (mismatch 1)
        rec_td = build_canonical_record("td-doc", "TEST_DATASHEET", {
            "project_code": "PRJ-101",
            "measured_value": "120 mm",
            "required_value": "150 mm",
            "unit": "mm",
            "quality_status": "compliant",
            "inspection_date": "2026-03-04"
        })
        
        # QM E-Form: quality_status is non-compliant (mismatch 2) and date is 2026-03-10 (mismatch 3)
        rec_qm = build_canonical_record("qm-doc", "QM_EFORM", {
            "project_code": "PRJ-101",
            "measured_value": "150 mm",
            "required_value": "150 mm",
            "unit": "mm",
            "quality_status": "non-compliant",
            "inspection_date": "2026-03-10"
        })
        
        discs = detect_discrepancies([rec_qcr, rec_td, rec_qm])
        
        # We expect at least:
        # - measured_value numerical mismatch
        # - quality_status text mismatch
        # - inspection_date mismatch
        fields_disc = [d["field"] for d in discs]
        self.assertIn("measured_value", fields_disc)
        self.assertIn("quality_status", fields_disc)
        self.assertIn("inspection_date", fields_disc)
        
        # Verify unique IDs exist and explanations are field-specific
        for d in discs:
            self.assertTrue(d["id"])
            explanation_lower = d["explanation"].lower()
            self.assertTrue(any(x in explanation_lower for x in ["value", "status", "date", "thickness", "field", "mismatch"]))
            self.assertTrue(d["severity"])

if __name__ == "__main__":
    unittest.main()
