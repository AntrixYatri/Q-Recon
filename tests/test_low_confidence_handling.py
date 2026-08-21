import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.data_integration.unified_data_builder import build_canonical_record
from ai_engine.discrepancy_engine.discrepancy_detector import detect_discrepancies

class TestLowConfidenceHandling(unittest.TestCase):
    def test_low_confidence_reduces_discrepancy_confidence(self):
        # 1. High confidence scenario
        rec_qcr_high = build_canonical_record("doc-1", "QCR", {"project_code": "PRJ-1", "measured_value": "150", "unit": "mm"}, {"ocr_confidence": 0.98})
        rec_td_high = build_canonical_record("doc-2", "TEST_DATASHEET", {"project_code": "PRJ-1", "measured_value": "120", "unit": "mm"}, {"ocr_confidence": 0.95})
        
        discs_high = detect_discrepancies([rec_qcr_high, rec_td_high])
        self.assertEqual(len(discs_high), 1)
        score_high = discs_high[0]["confidence"]
        
        # 2. Low confidence scenario
        rec_qcr_low = build_canonical_record("doc-1", "QCR", {"project_code": "PRJ-1", "measured_value": "150", "unit": "mm"}, {"ocr_confidence": 0.50})
        rec_td_low = build_canonical_record("doc-2", "TEST_DATASHEET", {"project_code": "PRJ-1", "measured_value": "120", "unit": "mm"}, {"ocr_confidence": 0.50})
        
        discs_low = detect_discrepancies([rec_qcr_low, rec_td_low])
        self.assertEqual(len(discs_low), 1)
        score_low = discs_low[0]["confidence"]
        
        # Compare
        print(f"High-conf discrepancy score: {score_high}, Low-conf score: {score_low}")
        self.assertLess(score_low, score_high)
        self.assertEqual(discs_low[0]["confidence_factors"]["ocr_confidence"], 0.50)

if __name__ == "__main__":
    unittest.main()
