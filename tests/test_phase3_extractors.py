import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.document_processing.document_classifier import classify_document
from ai_engine.document_processing.extractor_router import get_extractor
from ai_engine.document_processing.qcr_processor import QCRProcessor
from ai_engine.document_processing.test_datasheet_processor import TestDatasheetProcessor
from ai_engine.document_processing.qm_eform_processor import QMEFormProcessor
from ai_engine.pipeline import analyze_documents

class TestPhase3Extractors(unittest.TestCase):
    def test_document_classification(self):
        # 1. QCR classification (Task 14.1)
        res_qcr = classify_document("dummy_qcr.png", ocr_text="This is a Quality Control Register report")
        self.assertEqual(res_qcr["document_type"], "QCR")
        
        # 2. Test Datasheet classification (Task 14.2)
        res_td = classify_document("dummy_td.png", ocr_text="Laboratory Test Datasheet with material results")
        self.assertEqual(res_td["document_type"], "TEST_DATASHEET")

        # 3. QM E-Form classification (Task 14.3)
        res_qm = classify_document("dummy_qm.png", ocr_text="Quality Monitoring Inspection E-Form report")
        self.assertEqual(res_qm["document_type"], "QM_EFORM")

        # 4. Ambiguous / UNKNOWN document (Task 14.4 & 14.5)
        res_unk = classify_document("other.png", ocr_text="Random unrelated text content")
        self.assertEqual(res_unk["document_type"], "UNKNOWN")

    def test_extractor_registry(self):
        # Extractor registry selects correct processor (Task 14.10)
        self.assertIsInstance(get_extractor("QCR"), QCRProcessor)
        self.assertIsInstance(get_extractor("TEST_DATASHEET"), TestDatasheetProcessor)
        self.assertIsInstance(get_extractor("QM_EFORM"), QMEFormProcessor)
        self.assertIsNone(get_extractor("UNKNOWN_TYPE"))

    def test_processor_ocr_scaffolding(self):
        # Test Datasheet processor returns explicit not-implemented for raw OCR (Task 14.7)
        td_proc = TestDatasheetProcessor()
        res_td = td_proc.extract("raw_path.png")
        self.assertEqual(res_td["processing_status"], "failed")
        self.assertEqual(res_td["extracted_fields"], {})

        # QM E-Form processor returns explicit not-implemented (Task 14.8)
        qm_proc = QMEFormProcessor()
        res_qm = qm_proc.extract("raw_path.png")
        self.assertEqual(res_qm["processing_status"], "not_implemented")
        self.assertEqual(res_qm["extracted_fields"], {})

    def test_structured_input_bypass(self):
        # Structured input bypass works correctly (Task 14.9)
        td_proc = TestDatasheetProcessor()
        test_payload = {
            "document_id": "DS-99",
            "document_type": "TEST_DATASHEET",
            "fields": {"measured_value": "120"}
        }
        res_td = td_proc.extract(test_payload)
        self.assertEqual(res_td["processing_status"], "success")
        self.assertEqual(res_td["extracted_fields"]["measured_value"], "120")
        self.assertEqual(res_td["document_id"], "DS-99")

    def test_duplicate_document_ids_rejected(self):
        # Duplicate document IDs are rejected (Task 14.13)
        docs = [
            {"document_id": "DUP-1", "document_type": "QCR", "fields": {}},
            {"document_id": "DUP-1", "document_type": "TEST_DATASHEET", "fields": {}}
        ]
        res = analyze_documents(docs)
        self.assertEqual(res["processing_status"], "failed")
        self.assertIn("Duplicate document ID detected", res["error"])

    def test_mixed_mode_pipeline(self):
        # Mixed multi-document analysis works (Task 14.11)
        # We pass structured Test Datasheet & structured QM E-Form
        from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
        from ai_engine.testing.discrepancy_scenario_factory import create_scenario
        
        base_record = create_pmgsy_grounded_base_record(40, seed=42)
        all_docs = create_scenario(base_record, "numerical_mismatch")
        docs = all_docs[:2]
        
        res = analyze_documents(docs)
        self.assertEqual(res["processing_status"], "success")
        self.assertEqual(res["documents_analyzed"], 2)
        # Should detect a numerical mismatch discrepancy (150 mm vs 120 mm)
        self.assertEqual(len(res["discrepancies"]), 1)
        self.assertEqual(res["discrepancies"][0]["discrepancy_type"], "numerical_mismatch")

    def test_unknown_document_does_not_crash(self):
        # Unknown document does not crash a valid multi-document analysis (Task 14.12)
        docs = [
            # Valid structured document
            {
                "document_id": "TEST-QCR-01",
                "document_type": "QCR",
                "fields": {
                    "project_code": "PRJ-UNK",
                    "road_name": "Route 1",
                    "measured_value": "150"
                }
            },
            # Malformed/unsupported document type
            {
                "document_id": "TEST-UNK-01",
                "document_type": "INVALID_TYPE",
                "fields": {}
            }
        ]
        # Should raise validation error for unsupported type in structured validation
        # But what if it's a file path that gets classified as UNKNOWN?
        # Let's pass a path that gets classified as UNKNOWN
        # We can construct a list of inputs:
        docs_with_path = [
            {
                "document_id": "TEST-QCR-01",
                "document_type": "QCR",
                "fields": {
                    "project_code": "PRJ-UNK",
                    "road_name": "Route 1",
                    "measured_value": "150"
                }
            },
            # A raw path that does not exist (will fall back to filename classification and match UNKNOWN)
            {
                "path": "random_unsupported_file.png"
            }
        ]
        res = analyze_documents(docs_with_path)
        self.assertEqual(res["processing_status"], "success")
        self.assertEqual(res["documents_analyzed"], 1) # Only QCR was successfully processed
        self.assertEqual(len(res["warnings"]), 1)
        self.assertIn("skipped", res["warnings"][0])

if __name__ == "__main__":
    unittest.main()
