import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.data_integration.record_linker import link_records
from ai_engine.data_integration.unified_data_builder import build_canonical_record

class TestLinkingHardening(unittest.TestCase):
    def test_exact_match(self):
        rec_a = build_canonical_record("doc-1", "QCR", {"project_code": "PRJ-123", "road_name": "ABC Road"})
        rec_b = build_canonical_record("doc-2", "TEST_DATASHEET", {"project_code": "PRJ-123", "road_name": "ABC Road"})
        
        res = link_records(rec_a, rec_b)
        self.assertTrue(res["linked"])
        self.assertGreaterEqual(res["confidence"], 0.95)

    def test_case_variation(self):
        rec_a = build_canonical_record("doc-1", "QCR", {"project_code": "prj-123", "road_name": "abc road"})
        rec_b = build_canonical_record("doc-2", "TEST_DATASHEET", {"project_code": "PRJ-123", "road_name": "ABC Road"})
        
        res = link_records(rec_a, rec_b)
        self.assertTrue(res["linked"])

    def test_ocr_punctuation_variation(self):
        # "T.Narasipur" vs "T Narasipur" should match
        rec_a = build_canonical_record("doc-1", "QCR", {"project_code": "PRJ-123", "road_name": "T.Narasipur Link"})
        rec_b = build_canonical_record("doc-2", "TEST_DATASHEET", {"project_code": "PRJ-123", "road_name": "T Narasipur Link"})
        
        res = link_records(rec_a, rec_b)
        self.assertTrue(res["linked"])

    def test_missing_project_code_fallback(self):
        # Link using road_name + location signals
        rec_a = build_canonical_record("doc-1", "QCR", {"road_name": "Link Road", "district": "Tumkur", "block": "Madhugiri"})
        rec_b = build_canonical_record("doc-2", "TEST_DATASHEET", {"road_name": "Link Road", "district": "Tumkur", "block": "Madhugiri"})
        
        res = link_records(rec_a, rec_b)
        self.assertTrue(res["linked"])
        self.assertIn("road_name", res["matched_on"])

    def test_conflicting_project_codes(self):
        rec_a = build_canonical_record("doc-1", "QCR", {"project_code": "PRJ-123", "road_name": "ABC Road"})
        rec_b = build_canonical_record("doc-2", "TEST_DATASHEET", {"project_code": "PRJ-456", "road_name": "ABC Road"})
        
        res = link_records(rec_a, rec_b)
        self.assertFalse(res["linked"])

if __name__ == "__main__":
    unittest.main()
