import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.data_integration.unified_data_builder import build_canonical_record
from ai_engine.discrepancy_engine.discrepancy_detector import detect_discrepancies

class TestNormalizationStress(unittest.TestCase):
    def test_equivalent_units_no_discrepancy(self):
        # QCR has 150 mm
        rec_qcr = build_canonical_record("doc-1", "QCR", {
            "project_code": "PRJ-102",
            "measured_value": "150 mm",
            "required_value": "150 mm",
            "unit": "mm",
            "parameter": "Pavement Thickness"
        })
        
        # Test Datasheet has 15 cm
        rec_td = build_canonical_record("doc-2", "TEST_DATASHEET", {
            "project_code": "PRJ-102",
            "measured_value": "15",
            "required_value": "15",
            "unit": "cm",
            "parameter": "pavement thickness" # minor case difference
        })

        discs = detect_discrepancies([rec_qcr, rec_td])
        
        # There should be 0 discrepancies because 15 cm == 150 mm
        measured_disc = [d for d in discs if d["field"] == "measured_value"]
        self.assertEqual(len(measured_disc), 0)

    def test_equivalent_dates_no_discrepancy(self):
        # QCR date: 2026-03-04
        rec_qcr = build_canonical_record("doc-1", "QCR", {
            "project_code": "PRJ-102",
            "inspection_date": "2026-03-04"
        })
        
        # QM E-Form date: 04/03/2026 (DD/MM/YYYY)
        rec_qm = build_canonical_record("doc-2", "QM_EFORM", {
            "project_code": "PRJ-102",
            "inspection_date": "04/03/2026"
        })

        discs = detect_discrepancies([rec_qcr, rec_qm])
        
        # They normalize to the same ISO date "2026-03-04"
        date_disc = [d for d in discs if d["field"] == "inspection_date"]
        self.assertEqual(len(date_disc), 0)

if __name__ == "__main__":
    unittest.main()
