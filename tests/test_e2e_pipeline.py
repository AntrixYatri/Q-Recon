import unittest
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record, generate_document_variants
from ai_engine.testing.discrepancy_scenario_factory import create_scenario
from ai_engine.synthetic_documents.qcr_image_generator import generate_qcr_image
from ai_engine.pipeline import analyze_document, analyze_documents
from ai_engine.data_integration.unified_data_builder import build_canonical_record

class TestE2EPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate base QCR image from PMGSY record index 8
        cls.base_record = create_pmgsy_grounded_base_record(index=8, seed=42)
        # Ensure values are standard
        cls.base_record["measured_value"] = "150"
        cls.base_record["unit"] = "mm"
        cls.base_record["parameter"] = "Pavement Thickness"
        cls.base_record["required_value"] = "150"
        cls.base_record["quality_status"] = "COMPLIANT"
        
        cls.qcr_image_path = os.path.join(ROOT_DIR, "data", "synthetic", "e2e_test_qcr.png")
        generate_qcr_image(cls.base_record, cls.qcr_image_path)

        # Run OCR once and cache results
        cls.qcr_ocr_result_cached = analyze_document(cls.qcr_image_path)

    @classmethod
    def tearDownClass(cls):
        # Clean up generated test image
        if os.path.exists(cls.qcr_image_path):
            try:
                os.remove(cls.qcr_image_path)
            except Exception:
                pass

    def test_true_e2e_qcr_pipeline(self):
        # Verify document generation succeeds and file exists
        self.assertTrue(os.path.exists(self.qcr_image_path))
        
        # Run standard QCR document OCR, extraction, normalization pipeline
        import copy
        res = copy.deepcopy(self.qcr_ocr_result_cached)
        
        self.assertEqual(res.get("processing_status"), "success")
        self.assertEqual(res.get("document_type"), "QCR")
        
        # Verify key extracted fields match expected PMGSY base values (using case-insensitive/fuzzy match where OCR noise might occur)
        extracted = res.get("extracted_fields", {})
        
        # EasyOCR should capture these prominent fields from the generated image
        self.assertIn("state", extracted)
        self.assertIn("district", extracted)
        
        self.assertTrue(any(word in extracted.get("state", "") for word in ["karnataka", "karnatak"]))
        self.assertTrue(any(word in extracted.get("district", "") for word in ["dakshina", "kannada", "qakshina", "qanada"]))

    def test_true_multi_document_e2e_cases(self):
        # QCR is processed via image generation -> OCR -> extraction
        # Test Datasheet and QM E-Form are structured variants
        
        # 1. OCR QCR
        import copy
        qcr_ocr_result = copy.deepcopy(self.qcr_ocr_result_cached)
        self.assertEqual(qcr_ocr_result.get("processing_status"), "success")
        
        # Build document inputs list
        # Case A: all values consistent
        td_consistent = {
            "document_id": "e2e_test_td_a",
            "document_type": "TEST_DATASHEET",
            "fields": {
                "project_code": self.base_record["project_code"],
                "road_name": self.base_record["road_name"],
                "district": self.base_record["district"],
                "block": self.base_record["block"],
                "parameter": self.base_record["parameter"],
                "required_value": "15", # cm = 150 mm
                "measured_value": "15", # cm = 150 mm (Matches QCR!)
                "unit": "cm",
                "inspection_date": self.base_record["inspection_date"]
            }
        }
        
        qm_consistent = {
            "document_id": "e2e_test_qm_a",
            "document_type": "QM_EFORM",
            "fields": {
                "project_code": self.base_record["project_code"],
                "road_name": self.base_record["road_name"],
                "district": self.base_record["district"],
                "block": self.base_record["block"],
                "parameter": self.base_record["parameter"],
                "required_value": "150",
                "measured_value": "150",
                "unit": "mm",
                "inspection_date": self.base_record["inspection_date"],
                "quality_status": "COMPLIANT"
            }
        }
        
        # Build the inputs (combining QCR ocr result, structured TD and structured QM)
        # Note: analyze_documents accepts either path or dict. For QCR, we pass its ocr output structured dictionary.
        # We manually populate the quality parameter table and linking fields here because the raw OCR layout extractor 
        # only targets header metadata and doesn't extract table values in this phase.
        qcr_ocr_result["extracted_fields"]["measured_value"] = "150 mm"
        qcr_ocr_result["extracted_fields"]["required_value"] = "150 mm"
        qcr_ocr_result["extracted_fields"]["unit"] = "mm"
        qcr_ocr_result["extracted_fields"]["parameter"] = self.base_record["parameter"]
        
        # Populate linking fields so the record linker groups the documents together
        qcr_ocr_result["extracted_fields"]["project_code"] = self.base_record["project_code"]
        qcr_ocr_result["extracted_fields"]["road_name"] = self.base_record["road_name"]
        qcr_ocr_result["extracted_fields"]["habitation_id"] = self.base_record["habitation_id"]
        
        qcr_input = {
            "document_id": qcr_ocr_result["document_id"],
            "document_type": "QCR",
            "fields": qcr_ocr_result["extracted_fields"]
        }
        
        # CASE A: Consistent
        res_a = analyze_documents([qcr_input, td_consistent, qm_consistent])
        self.assertEqual(res_a["processing_status"], "success")
        
        # CASE B: Numerical mutation
        td_mutated = td_consistent.copy()
        td_mutated["fields"] = td_consistent["fields"].copy()
        td_mutated["fields"]["measured_value"] = "12" # 12 cm = 120 mm (Outlier!)
        
        res_b = analyze_documents([qcr_input, td_mutated, qm_consistent])
        self.assertEqual(res_b["processing_status"], "success")
        discs_b = res_b.get("discrepancies", [])
        
        # Verify a numerical mismatch was detected on measured_value
        has_num_mismatch = any(d["discrepancy_type"] == "numerical_mismatch" and d["field"] == "measured_value" for d in discs_b)
        self.assertTrue(has_num_mismatch)
 
        # CASE C: Majority consensus
        # QCR says 150 (derived via OCR), QM says 150, TD says 120. Outlier is TD.
        # Consensus should be 150.
        res_c = analyze_documents([qcr_input, td_mutated, qm_consistent])
        num_mismatch_disc = [d for d in res_c["discrepancies"] if d["field"] == "measured_value" and d["discrepancy_type"] == "numerical_mismatch"]
        if num_mismatch_disc:
            self.assertEqual(num_mismatch_disc[0]["metadata"].get("consensus_value"), "150")
 
        # CASE D: Ambiguous conflict (1 vs 1 mismatch on a field without authoritative source)
        td_mutated_date = td_mutated.copy()
        td_mutated_date["fields"] = td_mutated["fields"].copy()
        td_mutated_date["fields"]["inspection_date"] = "2026-08-19"
        
        qcr_input_date = qcr_input.copy()
        qcr_input_date["fields"] = qcr_input["fields"].copy()
        qcr_input_date["fields"]["inspection_date"] = "2026-08-10"
        
        res_d = analyze_documents([qcr_input_date, td_mutated_date]) # Only 2 documents
        has_ambiguous = any(d["discrepancy_type"] == "ambiguous_conflict" and d["field"] == "inspection_date" for d in res_d.get("discrepancies", []))
        self.assertTrue(has_ambiguous)

if __name__ == "__main__":
    unittest.main()
