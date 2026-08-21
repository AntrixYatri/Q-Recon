import unittest
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
from ai_engine.synthetic_documents.qcr_image_generator import generate_qcr_image
from ai_engine.synthetic_documents.test_datasheet_generator import generate_test_datasheet_image
from ai_engine.synthetic_documents.qm_eform_generator import generate_qm_eform_image
from ai_engine.pipeline import process_mixed_document, analyze_documents

class TestThreeDocumentE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_record = create_pmgsy_grounded_base_record(index=18, seed=42)
        cls.base_record["measured_value"] = "150"
        cls.base_record["unit"] = "mm"
        cls.base_record["parameter"] = "Pavement Thickness"
        cls.base_record["required_value"] = "150"
        cls.base_record["quality_status"] = "COMPLIANT"

        cls.qcr_path = os.path.join(ROOT_DIR, "data", "synthetic", "three_doc_qcr.png")
        cls.td_match_path = os.path.join(ROOT_DIR, "data", "synthetic", "three_doc_td.png")
        cls.qm_match_path = os.path.join(ROOT_DIR, "data", "synthetic", "three_doc_qm_match.png")
        cls.qm_mismatch_path = os.path.join(ROOT_DIR, "data", "synthetic", "three_doc_qm_mismatch.png")
        cls.qm_status_mismatch_path = os.path.join(ROOT_DIR, "data", "synthetic", "three_doc_qm_status_mismatch.png")

        # Generate QCR
        generate_qcr_image(cls.base_record, cls.qcr_path)

        # Generate Test Datasheet MATCH
        generate_test_datasheet_image(cls.base_record, cls.td_match_path, variant="B", seed=42)

        # Generate QM E-Form MATCH
        generate_qm_eform_image(cls.base_record, cls.qm_match_path, variant="B", seed=42)

        # Generate QM E-Form Outlier (120 mm)
        mismatch_record = cls.base_record.copy()
        mismatch_record["measured_value"] = "120"
        mismatch_record["quality_status"] = "NON-COMPLIANT"
        generate_qm_eform_image(mismatch_record, cls.qm_mismatch_path, variant="B", seed=42)

        # Generate QM E-Form Status Mismatch (150 mm but Non-Compliant status)
        status_mismatch_record = cls.base_record.copy()
        status_mismatch_record["quality_status"] = "NON-COMPLIANT"
        generate_qm_eform_image(status_mismatch_record, cls.qm_status_mismatch_path, variant="B", seed=42)

        # Pre-execute OCR for caching
        cls.qcr_res_cached = process_mixed_document(cls.qcr_path)
        cls.td_res_cached = process_mixed_document(cls.td_match_path)
        cls.qm_match_res_cached = process_mixed_document(cls.qm_match_path)
        cls.qm_mismatch_res_cached = process_mixed_document(cls.qm_mismatch_path)
        cls.qm_status_mismatch_res_cached = process_mixed_document(cls.qm_status_mismatch_path)

    @classmethod
    def tearDownClass(cls):
        paths = [
            cls.qcr_path, cls.td_match_path, cls.qm_match_path,
            cls.qm_mismatch_path, cls.qm_status_mismatch_path
        ]
        for path in paths:
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

    def _prepare_qcr_ocr_result(self) -> dict:
        import copy
        qcr_res = copy.deepcopy(self.qcr_res_cached)
        self.assertEqual(qcr_res["processing_status"], "success")
        # Populate table and linking fields manually for QCR as layout OCR in this phase is metadata-focused
        qcr_res["extracted_fields"]["measured_value"] = "150 mm"
        qcr_res["extracted_fields"]["required_value"] = "150 mm"
        qcr_res["extracted_fields"]["unit"] = "mm"
        qcr_res["extracted_fields"]["parameter"] = self.base_record["parameter"]
        qcr_res["extracted_fields"]["project_code"] = self.base_record["project_code"]
        qcr_res["extracted_fields"]["road_name"] = self.base_record["road_name"]
        qcr_res["extracted_fields"]["habitation_id"] = self.base_record["habitation_id"]
        qcr_res["extracted_fields"]["quality_status"] = "compliant"
        return qcr_res

    def _to_input(self, res, doc_type) -> dict:
        return {
            "document_id": res["document_id"],
            "document_type": doc_type,
            "fields": res["extracted_fields"]
        }

    def test_case_a_full_match(self):
        # All three documents match
        import copy
        qcr_res = self._prepare_qcr_ocr_result()
        td_res = copy.deepcopy(self.td_res_cached)
        qm_res = copy.deepcopy(self.qm_match_res_cached)

        docs = [
            self._to_input(qcr_res, "QCR"),
            self._to_input(td_res, "TEST_DATASHEET"),
            self._to_input(qm_res, "QM_EFORM")
        ]
        analysis = analyze_documents(docs)
        self.assertEqual(analysis["processing_status"], "success")
        self.assertEqual(analysis["summary"]["total_discrepancies"], 0)

    def test_case_b_numerical_outlier(self):
        # QM E-Form is outlier (120 mm vs 150 mm in others)
        import copy
        qcr_res = self._prepare_qcr_ocr_result()
        td_res = copy.deepcopy(self.td_res_cached)
        qm_res = copy.deepcopy(self.qm_mismatch_res_cached)

        docs = [
            self._to_input(qcr_res, "QCR"),
            self._to_input(td_res, "TEST_DATASHEET"),
            self._to_input(qm_res, "QM_EFORM")
        ]
        analysis = analyze_documents(docs)
        self.assertEqual(analysis["processing_status"], "success")
        
        measured_disc = [d for d in analysis["discrepancies"] if d["field"] == "measured_value"]
        self.assertEqual(len(measured_disc), 1)
        self.assertEqual(measured_disc[0]["discrepancy_type"], "numerical_mismatch")
        
        # Outlier detection should point to the mismatch file
        explanation = measured_disc[0]["explanation"]
        self.assertIn("three_doc_qm_mismatch.png", explanation)

    def test_case_c_status_mismatch(self):
        # QM E-Form says Non-Compliant, while others say Compliant
        import copy
        qcr_res = self._prepare_qcr_ocr_result()
        td_res = copy.deepcopy(self.td_res_cached)
        qm_res = copy.deepcopy(self.qm_status_mismatch_res_cached)

        docs = [
            self._to_input(qcr_res, "QCR"),
            self._to_input(td_res, "TEST_DATASHEET"),
            self._to_input(qm_res, "QM_EFORM")
        ]
        analysis = analyze_documents(docs)
        self.assertEqual(analysis["processing_status"], "success")
        
        status_disc = [d for d in analysis["discrepancies"] if d["field"] == "quality_status" and d["discrepancy_type"] == "text_mismatch"]
        self.assertEqual(len(status_disc), 1)
        self.assertEqual(status_disc[0]["discrepancy_type"], "text_mismatch")

    def test_case_d_missing_required_field(self):
        # Test Datasheet matches QCR, but QM E-Form is missing measured_value
        import copy
        qcr_res = self._prepare_qcr_ocr_result()
        td_res = copy.deepcopy(self.td_res_cached)
        
        qm_res = copy.deepcopy(self.qm_match_res_cached)
        # Delete measured_value in qm_res to simulate missing field
        if "measured_value" in qm_res["extracted_fields"]:
            del qm_res["extracted_fields"]["measured_value"]

        docs = [
            self._to_input(qcr_res, "QCR"),
            self._to_input(td_res, "TEST_DATASHEET"),
            self._to_input(qm_res, "QM_EFORM")
        ]
        analysis = analyze_documents(docs)
        self.assertEqual(analysis["processing_status"], "success")
        
        missing_disc = [d for d in analysis["discrepancies"] if d["field"] == "measured_value" and d["discrepancy_type"] == "missing_value"]
        self.assertEqual(len(missing_disc), 1)

if __name__ == "__main__":
    unittest.main()
