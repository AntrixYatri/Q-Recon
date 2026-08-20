import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.data_integration.canonical_schema import CanonicalRecord
from ai_engine.data_integration.record_linker import link_records, group_records

class TestRecordLinking(unittest.TestCase):
    def test_link_by_project_code(self):
        rec_a = CanonicalRecord()
        rec_a.set_field("project_code", "PRJ-101", "QCR", "project_code")
        
        rec_b = CanonicalRecord()
        rec_b.set_field("project_code", "PRJ-101", "TEST_DATASHEET", "project_code")
        
        res = link_records(rec_a, rec_b)
        self.assertTrue(res["linked"])
        self.assertGreaterEqual(res["confidence"], 0.95)
        self.assertIn("project_code", res["matched_on"])

    def test_link_by_road_name_location(self):
        rec_a = CanonicalRecord()
        rec_a.set_field("road_name", "Route 4 Bypass", "QCR", "road_name")
        rec_a.set_field("district", "Belagavi", "QCR", "district")
        rec_a.set_field("block", "Athni", "QCR", "block")
        
        rec_b = CanonicalRecord()
        # Case mismatch is handled by normalize_field_value inside linker
        rec_b.set_field("road_name", "route 4 bypass", "TEST_DATASHEET", "road")
        rec_b.set_field("district", "belagavi", "TEST_DATASHEET", "district")
        rec_b.set_field("block", "athni", "TEST_DATASHEET", "block")
        
        res = link_records(rec_a, rec_b)
        self.assertTrue(res["linked"])
        self.assertIn("road_name", res["matched_on"])
        self.assertIn("district", res["matched_on"])
        self.assertIn("block", res["matched_on"])

    def test_group_records_disconnected(self):
        rec_a = CanonicalRecord()
        rec_a.set_field("project_code", "PRJ-101", "QCR", "project_code")
        
        rec_b = CanonicalRecord()
        rec_b.set_field("project_code", "PRJ-999", "QCR", "project_code")
        
        groups = group_records([rec_a, rec_b])
        self.assertEqual(len(groups), 2)

if __name__ == "__main__":
    unittest.main()
