import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.document_processing.layout_field_extractor import extract_from_reconstructed_lines
from ai_engine.extraction.key_value_extractor import extract_key_values_from_lines
from ai_engine.preprocessing.field_normalizer import normalize_field_value
from ai_engine.pipeline import process_mixed_document

class TestHardcodingProof(unittest.TestCase):
    def test_changed_value(self):
        # Test 1 - Changed value test
        # Input has a custom road length '8.7 km'
        lines = [
            {"text": "Road Name: Link Road Alpha"},
            {"text": "Road Length: 8.7 km"},
            {"text": "Road Category: Rural Road"}
        ]
        res = extract_key_values_from_lines(lines)
        self.assertEqual(res.get("road_length"), "8.7 km")

    def test_unseen_name(self):
        # Test 2 - Unseen name test
        # Input has a new inspector name 'Mr. Rajan Kumar'
        lines = [
            {"text": "Inspector Name: Mr. Rajan Kumar"},
            {"text": "Inspection Date: 2026-08-21"}
        ]
        res = extract_key_values_from_lines(lines)
        self.assertEqual(res.get("inspector_name"), "Mr. Rajan Kumar")

    def test_new_state(self):
        # Test 3 - New state test
        # Maharashtra
        lines_mh = [
            {"text": "State: Maharashtra"},
            {"text": "District: Nagpur"}
        ]
        res_mh = extract_key_values_from_lines(lines_mh)
        self.assertEqual(res_mh.get("state"), "Maharashtra")
        
        # Tamil Nadu
        lines_tn = [
            {"text": "State Name: Tamil Nadu"},
            {"text": "District: Chennai"}
        ]
        res_tn = extract_key_values_from_lines(lines_tn)
        self.assertEqual(res_tn.get("state"), "Tamil Nadu")

    def test_missing_field(self):
        # Test 4 - Missing field test
        # Input lacks 'measured_value' completely
        lines = [
            {"text": "Parameter: Pavement Thickness"},
            {"text": "Required Value: 150"}
        ]
        res = extract_key_values_from_lines(lines)
        self.assertIsNone(res.get("measured_value"))

    def test_layout_variation(self):
        # Test 5 - Layout variation test
        # Verify that extraction handles spacing, colons, vertical position changes
        lines_var = [
            {"text": "Project Code     PRJ-99999"}, # double spaces, no colon
            {"text": "Road Name:     Link Road Beta"}, # extra spaces after colon
            {"text": "Inspection Date"}, # multi-line key-value
            {"text": "15 Aug 2026"}
        ]
        res = extract_key_values_from_lines(lines_var)
        self.assertEqual(res.get("project_code"), "PRJ-99999")
        self.assertEqual(res.get("road_name"), "Link Road Beta")
        self.assertEqual(res.get("inspection_date"), "15 Aug 2026")

if __name__ == "__main__":
    unittest.main()
