import unittest
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
from ai_engine.synthetic_documents.qcr_image_generator import generate_qcr_image
from ai_engine.synthetic_documents.test_datasheet_generator import generate_test_datasheet_image
from ai_engine.pipeline import process_mixed_document, analyze_documents
from ai_engine.document_processing.document_classifier import classify_document

class TestTestDatasheetE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate base record
        cls.base_record = create_pmgsy_grounded_base_record(index=15, seed=42)
        cls.base_record["measured_value"] = "150"
        cls.base_record["unit"] = "mm"
        cls.base_record["parameter"] = "Pavement Thickness"
        cls.base_record["required_value"] = "150"
        cls.base_record["quality_status"] = "COMPLIANT"

        cls.qcr_path = os.path.join(ROOT_DIR, "data", "synthetic", "e2e_td_qcr.png")
        cls.td_match_path = os.path.join(ROOT_DIR, "data", "synthetic", "e2e_td_match.png")
        cls.td_mismatch_path = os.path.join(ROOT_DIR, "data", "synthetic", "e2e_td_mismatch.png")

        # Generate QCR
        generate_qcr_image(cls.base_record, cls.qcr_path)

        # Generate Test Datasheet MATCH (150 mm)
        generate_test_datasheet_image(cls.base_record, cls.td_match_path, variant="B", seed=42)

        # Generate Test Datasheet MISMATCH (120 mm)
        mismatch_record = cls.base_record.copy()
        mismatch_record["measured_value"] = "120"
        mismatch_record["quality_status"] = "NON-COMPLIANT"
        generate_test_datasheet_image(mismatch_record, cls.td_mismatch_path, variant="B", seed=42)

        # Run OCR once and cache results
        cls.classification_res_cached = classify_document(cls.td_match_path)
        cls.qcr_res_cached = process_mixed_document(cls.qcr_path)
        cls.td_match_res_cached = process_mixed_document(cls.td_match_path)
        cls.td_mismatch_res_cached = process_mixed_document(cls.td_mismatch_path)

    @classmethod
    def tearDownClass(cls):
        # Cleanup
        for path in [cls.qcr_path, cls.td_match_path, cls.td_mismatch_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
            json_path = os.path.splitext(path)[0] + ".json"
            if os.path.exists(json_path):
                try:
                    os.remove(json_path)
                except Exception:
                    pass

    def test_document_classification(self):
        # Verify Test Datasheet image is classified correctly
        res = self.classification_res_cached
        self.assertEqual(res["document_type"], "TEST_DATASHEET")

    def test_case_a_match(self):
        # Case A: QCR (150 mm) vs Test Datasheet (150 mm)
        import copy
        qcr_res = copy.deepcopy(self.qcr_res_cached)
        td_res = copy.deepcopy(self.td_match_res_cached)
        
        self.assertEqual(qcr_res["processing_status"], "success")
        self.assertEqual(td_res["processing_status"], "success")
        
        # We manually populate table fields for QCR inside E2E tests
        # because the raw QCR OCR only extracts headers in this phase.
        qcr_res["extracted_fields"]["measured_value"] = "150 mm"
        qcr_res["extracted_fields"]["required_value"] = "150 mm"
        qcr_res["extracted_fields"]["unit"] = "mm"
        qcr_res["extracted_fields"]["parameter"] = self.base_record["parameter"]
        qcr_res["extracted_fields"]["project_code"] = self.base_record["project_code"]
        qcr_res["extracted_fields"]["road_name"] = self.base_record["road_name"]
        
        docs = [
            {
                "document_id": qcr_res["document_id"],
                "document_type": "QCR",
                "fields": qcr_res["extracted_fields"]
            },
            {
                "document_id": td_res["document_id"],
                "document_type": "TEST_DATASHEET",
                "fields": td_res["extracted_fields"]
            }
        ]
        
        analysis = analyze_documents(docs)
        self.assertEqual(analysis["processing_status"], "success")
        
        # Since they are matched, no discrepancy should be found on measured_value
        measured_disc = [d for d in analysis["discrepancies"] if d["field"] == "measured_value"]
        self.assertEqual(len(measured_disc), 0)

    def test_case_b_mismatch(self):
        # Case B: QCR (150 mm) vs Test Datasheet (120 mm)
        import copy
        qcr_res = copy.deepcopy(self.qcr_res_cached)
        td_res = copy.deepcopy(self.td_mismatch_res_cached)
        
        self.assertEqual(qcr_res["processing_status"], "success")
        self.assertEqual(td_res["processing_status"], "success")
        
        # Verify Test Datasheet's value is extracted as 120 or 120 mm
        qcr_res["extracted_fields"]["measured_value"] = "150 mm"
        qcr_res["extracted_fields"]["required_value"] = "150 mm"
        qcr_res["extracted_fields"]["unit"] = "mm"
        qcr_res["extracted_fields"]["parameter"] = self.base_record["parameter"]
        qcr_res["extracted_fields"]["project_code"] = self.base_record["project_code"]
        qcr_res["extracted_fields"]["road_name"] = self.base_record["road_name"]
        
        docs = [
            {
                "document_id": qcr_res["document_id"],
                "document_type": "QCR",
                "fields": qcr_res["extracted_fields"]
            },
            {
                "document_id": td_res["document_id"],
                "document_type": "TEST_DATASHEET",
                "fields": td_res["extracted_fields"]
            }
        ]
        
        analysis = analyze_documents(docs)
        self.assertEqual(analysis["processing_status"], "success")
        
        # A discrepancy of type numerical_mismatch should be detected on measured_value
        measured_disc = [d for d in analysis["discrepancies"] if d["field"] == "measured_value"]
        self.assertEqual(len(measured_disc), 1)
        self.assertEqual(measured_disc[0]["discrepancy_type"], "numerical_mismatch")
        self.assertEqual(measured_disc[0]["metadata"].get("consensus_value"), "150")

if __name__ == "__main__":
    unittest.main()
