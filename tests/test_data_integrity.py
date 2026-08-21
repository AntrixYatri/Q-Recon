import unittest
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record, generate_document_variants
from ai_engine.testing.discrepancy_scenario_factory import create_scenario
from ai_engine.testing.dataset_loader import load_pmgsy_grounded_records, select_deterministic_record
from ai_engine.synthetic_documents.qcr_image_generator import generate_qcr_image

class TestDataIntegrity(unittest.TestCase):
    def test_fixture_provenance(self):
        # 1. Integration fixture provenance is present and marked PMGSY-grounded
        # 2. Selected fixture can be traced to a real row
        base_record = create_pmgsy_grounded_base_record(index=2, seed=42)
        self.assertIn("provenance", base_record)
        
        prov = base_record["provenance"]
        self.assertEqual(prov["data_origin"], "pmgsy_grounded_synthetic")
        self.assertEqual(prov["source_dataset"], "pmgsy_karnataka_100.csv")
        self.assertEqual(prov["generator"], "pmgsy_qcr_generator")
        
        # Verify it traces to a real row
        records = load_pmgsy_grounded_records()
        row_index = prov["source_row_index"]
        original_row = records[row_index]
        
        # Verify base fields match the original PMGSY source row columns
        self.assertEqual(base_record["state"], original_row["State"])
        self.assertEqual(base_record["district"], original_row["District"])
        self.assertEqual(base_record["block"], original_row["Block"])
        self.assertEqual(base_record["habitation_name"], original_row["Habitation Name"])
        self.assertEqual(str(base_record["habitation_id"]), str(original_row["Habitation ID"]))

    def test_scenario_mutation_preserves_identity(self):
        # 3. Scenario mutation preserves original project/road identity
        # 4. Only intended fields change during controlled discrepancy generation
        base_record = create_pmgsy_grounded_base_record(index=4, seed=42)
        
        # Check formatting_difference scenario
        scenario_docs = create_scenario(base_record, "formatting_difference")
        qcr, td, qm = scenario_docs[0], scenario_docs[1], scenario_docs[2]
        
        # Identifiers must be preserved
        self.assertEqual(qcr["fields"]["project_code"], base_record["project_code"])
        self.assertEqual(td["fields"]["project_code"], base_record["project_code"])
        self.assertEqual(qm["fields"]["project_code"], base_record["project_code"])
        
        self.assertEqual(qcr["fields"]["habitation_id"], base_record["habitation_id"])
        self.assertEqual(td["fields"]["habitation_id"], base_record["habitation_id"])
        self.assertEqual(qm["fields"]["habitation_id"], base_record["habitation_id"])

        # Check numerical_mismatch scenario
        scenario_docs_num = create_scenario(base_record, "numerical_mismatch")
        qcr_num, td_num, qm_num = scenario_docs_num[0], scenario_docs_num[1], scenario_docs_num[2]
        
        # The mutated field is measured_value (which changes to 120 in DS variant)
        self.assertEqual(qcr_num["fields"]["measured_value"], "150")
        self.assertEqual(td_num["fields"]["measured_value"], "120")
        self.assertEqual(qm_num["fields"]["measured_value"], "150")
        
        # Unrelated fields like project_code, habitation_id, state must remain unchanged
        self.assertEqual(td_num["fields"]["project_code"], base_record["project_code"])
        self.assertEqual(td_num["fields"]["habitation_id"], base_record["habitation_id"])
        self.assertEqual(td_num["fields"]["district"], base_record["district"])
        self.assertEqual(td_num["fields"]["block"], base_record["block"])

    def test_synthetic_document_generation_uses_fixture(self):
        # 5. Synthetic document generation uses the PMGSY-grounded fixture
        base_record = create_pmgsy_grounded_base_record(index=6, seed=42)
        
        temp_img_path = os.path.join(ROOT_DIR, "data", "synthetic", "test_integrity_qcr.png")
        if os.path.exists(temp_img_path):
            try:
                os.remove(temp_img_path)
            except Exception:
                pass
                
        generate_qcr_image(base_record, temp_img_path)
        self.assertTrue(os.path.exists(temp_img_path))
        
        # Clean up
        try:
            os.remove(temp_img_path)
        except Exception:
            pass

    def test_generic_qcr_generator_not_accidental_origin(self):
        # 6. Generic qcr_generator output is not accidentally used by PMGSY-grounded tests
        from ai_engine.data_generation.qcr_generator import generate_qcr_record
        generic_rec = generate_qcr_record(1)
        self.assertNotIn("provenance", generic_rec)
        
        pmgsy_rec = create_pmgsy_grounded_base_record(index=1, seed=42)
        self.assertIn("provenance", pmgsy_rec)
        self.assertEqual(pmgsy_rec["provenance"]["data_origin"], "pmgsy_grounded_synthetic")

if __name__ == "__main__":
    unittest.main()
