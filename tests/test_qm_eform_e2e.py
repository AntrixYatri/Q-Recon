import unittest
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
from ai_engine.synthetic_documents.qm_eform_generator import generate_qm_eform_image
from ai_engine.pipeline import process_mixed_document, analyze_documents
from ai_engine.document_processing.document_classifier import classify_document

class TestQMEFormE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate base record
        cls.base_record = create_pmgsy_grounded_base_record(index=16, seed=42)
        cls.base_record["measured_value"] = "150"
        cls.base_record["unit"] = "mm"
        cls.base_record["parameter"] = "Pavement Thickness"
        cls.base_record["required_value"] = "150"
        cls.base_record["quality_status"] = "COMPLIANT"

        cls.qm_match_path = os.path.join(ROOT_DIR, "data", "synthetic", "e2e_qm_match.png")
        cls.qm_mismatch_path = os.path.join(ROOT_DIR, "data", "synthetic", "e2e_qm_mismatch.png")

        # Generate QM E-Form MATCH
        generate_qm_eform_image(cls.base_record, cls.qm_match_path, variant="B", seed=42)

        # Generate QM E-Form MISMATCH (120 mm, Non-compliant status)
        mismatch_record = cls.base_record.copy()
        mismatch_record["measured_value"] = "120"
        mismatch_record["quality_status"] = "NON-COMPLIANT"
        generate_qm_eform_image(mismatch_record, cls.qm_mismatch_path, variant="B", seed=42)

        # Run OCR and classification once and cache results
        cls.classification_res_cached = classify_document(cls.qm_match_path)
        cls.qm_match_res_cached = process_mixed_document(cls.qm_match_path)
        cls.qm_mismatch_res_cached = process_mixed_document(cls.qm_mismatch_path)

    @classmethod
    def tearDownClass(cls):
        for path in [cls.qm_match_path, cls.qm_mismatch_path]:
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
        res = self.classification_res_cached
        self.assertEqual(res["document_type"], "QM_EFORM")

    def test_extraction_correctness(self):
        import copy
        res = copy.deepcopy(self.qm_match_res_cached)
        self.assertEqual(res["processing_status"], "success")
        
        extracted = res["extracted_fields"]
        self.assertEqual(extracted.get("project_code").lower(), self.base_record["project_code"].lower())
        self.assertEqual(extracted.get("road_name").lower(), self.base_record["road_name"].lower())
        self.assertEqual(extracted.get("measured_value"), "150")
        self.assertEqual(extracted.get("unit"), "mm")
        self.assertEqual(extracted.get("quality_status"), "compliant")

    def test_mismatch_extraction(self):
        import copy
        res = copy.deepcopy(self.qm_mismatch_res_cached)
        self.assertEqual(res["processing_status"], "success")
        
        extracted = res["extracted_fields"]
        self.assertEqual(extracted.get("measured_value"), "120")
        self.assertEqual(extracted.get("quality_status"), "non-compliant")

if __name__ == "__main__":
    unittest.main()
