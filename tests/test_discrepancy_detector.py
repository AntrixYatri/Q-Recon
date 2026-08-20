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
        rec_a = CanonicalRecord()
        rec_a.set_field("project_code", "PRJ-101", "QCR", "project_code")
        rec_a.set_field("road_name", "Route A", "QCR", "road_name")
        rec_a.set_field("measured_value", "150", "QCR", "measured_value")
        rec_a.set_field("unit", "mm", "QCR", "unit")

        rec_b = CanonicalRecord()
        rec_b.set_field("project_code", "PRJ-101", "TEST_DATASHEET", "project_code")
        rec_b.set_field("road_name", "Route A", "TEST_DATASHEET", "road")
        rec_b.set_field("measured_value", "150", "TEST_DATASHEET", "measured_value")
        rec_b.set_field("unit", "mm", "TEST_DATASHEET", "unit")

        discrepancies = detect_discrepancies([rec_a, rec_b])
        self.assertEqual(len(discrepancies), 0)

    def test_numerical_mismatch(self):
        # Case 4: Numerical mismatch -> 1 numerical mismatch
        rec_a = CanonicalRecord()
        rec_a.set_field("project_code", "PRJ-101", "QCR", "project_code")
        rec_a.set_field("road_name", "Route A", "QCR", "road_name")
        rec_a.set_field("measured_value", "150", "QCR", "measured_value")
        rec_a.set_field("unit", "mm", "QCR", "unit")

        rec_b = CanonicalRecord()
        rec_b.set_field("project_code", "PRJ-101", "TEST_DATASHEET", "project_code")
        rec_b.set_field("road_name", "Route A", "TEST_DATASHEET", "road")
        rec_b.set_field("measured_value", "120", "TEST_DATASHEET", "measured_value")
        rec_b.set_field("unit", "mm", "TEST_DATASHEET", "unit")

        discrepancies = detect_discrepancies([rec_a, rec_b])
        self.assertEqual(len(discrepancies), 1)
        self.assertEqual(discrepancies[0]["discrepancy_type"], "numerical_mismatch")

if __name__ == "__main__":
    unittest.main()
