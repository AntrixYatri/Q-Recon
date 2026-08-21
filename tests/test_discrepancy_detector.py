import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.data_integration.canonical_schema import CanonicalRecord
from ai_engine.discrepancy_engine.discrepancy_detector import detect_discrepancies

class TestDiscrepancyDetector(unittest.TestCase):
    def test_identical_records_zero_discrepancies(self):
        # Case 1: Identical documents -> 0 discrepancies
        from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record, generate_document_variants
        from ai_engine.data_integration.unified_data_builder import build_canonical_record
        
        base_record = create_pmgsy_grounded_base_record(3, seed=42)
        variants = generate_document_variants(base_record)
        
        rec_a = build_canonical_record(variants["QCR"]["document_id"], "QCR", variants["QCR"]["fields"])
        rec_b = build_canonical_record(variants["TEST_DATASHEET"]["document_id"], "TEST_DATASHEET", variants["TEST_DATASHEET"]["fields"])

        discrepancies = detect_discrepancies([rec_a, rec_b])
        self.assertEqual(len(discrepancies), 0)

    def test_numerical_mismatch(self):
        # Case 4: Numerical mismatch -> 1 numerical mismatch
        from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record, generate_document_variants
        from ai_engine.data_integration.unified_data_builder import build_canonical_record
        
        base_record = create_pmgsy_grounded_base_record(3, seed=42)
        variants = generate_document_variants(base_record)
        
        # Mutate measured value to create discrepancy
        variants["TEST_DATASHEET"]["fields"]["measured_value"] = "120"
        variants["TEST_DATASHEET"]["fields"]["unit"] = "mm"
        
        rec_a = build_canonical_record(variants["QCR"]["document_id"], "QCR", variants["QCR"]["fields"])
        rec_b = build_canonical_record(variants["TEST_DATASHEET"]["document_id"], "TEST_DATASHEET", variants["TEST_DATASHEET"]["fields"])

        discrepancies = detect_discrepancies([rec_a, rec_b])
        self.assertEqual(len(discrepancies), 1)
        self.assertEqual(discrepancies[0]["discrepancy_type"], "numerical_mismatch")

if __name__ == "__main__":
    unittest.main()
