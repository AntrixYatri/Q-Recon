import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.data_integration.canonical_schema import CanonicalRecord
from ai_engine.discrepancy_engine.discrepancy_detector import detect_discrepancies, compare_documents
from ai_engine.scoring.confidence_calculator import calculate_confidence
from ai_engine.scoring.severity_calculator import calculate_severity
from backend.app.services.analysis_service import AnalysisService

class TestPhase21Hardened(unittest.TestCase):
    def test_confidence_limit_range(self):
        # 1. OCR average / linking confidence should remain in 0.0 - 1.0
        disc = {
            "documents": [
                {"ocr_confidence": 95.0}, # check that we handle percentage inputs correctly
                {"ocr_confidence": 0.92}
            ]
        }
        res = calculate_confidence(disc)
        self.assertGreaterEqual(res["confidence_score"], 0.0)
        self.assertLessEqual(res["confidence_score"], 1.0)
        # Ensure we do not perform percentage conversion inside the AI engine (Task 8.3)
        self.assertEqual(res["confidence_score"], 0.89) # (0.95 + 0.92)/2 * 0.95 rounded to 2 decimals

    def test_2_document_disagreement_tie(self):
        # 2-document disagreement with no authority results in ambiguous conflict (Task 8.4)
        rec_a = CanonicalRecord()
        rec_a.set_field("document_id", "DOC-A", "QCR", "document_id")
        rec_a.set_field("document_type", "QCR", "QCR", "document_type")
        rec_a.set_field("project_code", "PRJ-TIE", "QCR", "project_code")
        rec_a.set_field("road_name", "Route A", "QCR", "road_name")
        rec_a.set_field("inspection_date", "2026-08-10", "QCR", "inspection_date")

        rec_b = CanonicalRecord()
        rec_b.set_field("document_id", "DOC-B", "TEST_DATASHEET", "document_id")
        rec_b.set_field("document_type", "TEST_DATASHEET", "TEST_DATASHEET", "document_type")
        rec_b.set_field("project_code", "PRJ-TIE", "TEST_DATASHEET", "project_code")
        rec_b.set_field("road_name", "Route A", "TEST_DATASHEET", "road")
        rec_b.set_field("inspection_date", "2026-08-15", "TEST_DATASHEET", "inspection_date")

        discrepancies = detect_discrepancies([rec_a, rec_b])
        # Should generate an ambiguous conflict
        self.assertEqual(len(discrepancies), 1)
        self.assertEqual(discrepancies[0]["discrepancy_type"], "ambiguous_conflict")
        self.assertEqual(discrepancies[0]["comparison_status"], "ambiguous")

    def test_3_document_disagreement_majority(self):
        # 3-document disagreement (150, 150, 120) -> 150 consensus, 120 outlier (Task 8.5)
        rec_a = CanonicalRecord()
        rec_a.set_field("document_id", "DOC-A", "QCR", "document_id")
        rec_a.set_field("document_type", "QCR", "QCR", "document_type")
        rec_a.set_field("project_code", "PRJ-MAJ", "QCR", "project_code")
        rec_a.set_field("road_name", "Route A", "QCR", "road_name")
        rec_a.set_field("measured_value", "150", "QCR", "measured_value")

        rec_b = CanonicalRecord()
        rec_b.set_field("document_id", "DOC-B", "TEST_DATASHEET", "document_id")
        rec_b.set_field("document_type", "TEST_DATASHEET", "TEST_DATASHEET", "document_type")
        rec_b.set_field("project_code", "PRJ-MAJ", "TEST_DATASHEET", "project_code")
        rec_b.set_field("road_name", "Route A", "TEST_DATASHEET", "road")
        rec_b.set_field("measured_value", "120", "TEST_DATASHEET", "measured_value")

        rec_c = CanonicalRecord()
        rec_c.set_field("document_id", "DOC-C", "QM_EFORM", "document_id")
        rec_c.set_field("document_type", "QM_EFORM", "QM_EFORM", "document_type")
        rec_c.set_field("project_code", "PRJ-MAJ", "QM_EFORM", "project_code")
        rec_c.set_field("road_name", "Route A", "QM_EFORM", "road_name")
        rec_c.set_field("measured_value", "150", "QM_EFORM", "measured_value")

        discrepancies = detect_discrepancies([rec_a, rec_b, rec_c])
        self.assertEqual(len(discrepancies), 1)
        self.assertEqual(discrepancies[0]["discrepancy_type"], "numerical_mismatch")
        self.assertEqual(discrepancies[0]["comparison_status"], "mismatch")
        # Consensus value is 150
        self.assertEqual(discrepancies[0]["metadata"]["consensus_value"], "150")

    def test_summary_and_id_consistency(self):
        # Summary counts equal actual discrepancy list (Task 8.6)
        # Duplicate discrepancy IDs cannot occur (Task 8.7)
        res = compare_documents("proj-101")
        summary = res["summary"]
        discrepancies = res["discrepancies"]
        
        self.assertEqual(summary["total_discrepancies"], len(discrepancies))
        
        calculated_total = summary["critical"] + summary["high"] + summary["medium"] + summary["low"]
        self.assertEqual(summary["total_discrepancies"], calculated_total)

        # Check unique IDs
        ids = [d["id"] for d in discrepancies]
        self.assertEqual(len(ids), len(set(ids)))

    def test_api_severity_confidence_consistency(self):
        # Severity and confidence remain consistent from AI pipeline to FastAPI (Task 8.1 & 8.2)
        api_res = AnalysisService.run_analysis("proj-101")
        summary = api_res["summary"]
        discrepancies = api_res["discrepancies"]

        self.assertEqual(summary["total_discrepancies"], len(discrepancies))
        calculated_total = summary["critical"] + summary["high"] + summary["medium"] + summary["low"]
        self.assertEqual(summary["total_discrepancies"], calculated_total)

        for disc in discrepancies:
            # Must be lowercase externally
            self.assertIn(disc["severity"], ["critical", "high", "warning", "minor", "low", "medium"])
            # Confidence must be decimal float between 0.0 and 1.0
            self.assertLessEqual(disc["confidence"], 1.0)
            self.assertGreaterEqual(disc["confidence"], 0.0)

if __name__ == "__main__":
    unittest.main()
