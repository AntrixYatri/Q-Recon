import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.discrepancy_engine.text_comparator import compare_text_values

class TestTextComparison(unittest.TestCase):
    def test_exact_match(self):
        res = compare_text_values("Karnataka", "Karnataka")
        self.assertTrue(res["match"])
        self.assertEqual(res["match_type"], "exact_match")

    def test_normalized_match(self):
        # Case and whitespace variations
        res = compare_text_values("Karnataka ", "karnataka")
        self.assertTrue(res["match"])
        self.assertEqual(res["match_type"], "normalized_match")

    def test_probable_match(self):
        # Spelling mistake: 'Karnatka' vs 'Karnataka'
        res = compare_text_values("Karnatka", "Karnataka")
        self.assertTrue(res["match"])
        self.assertEqual(res["match_type"], "probable_match")
        self.assertGreater(res["similarity"], 0.82)

    def test_mismatch(self):
        res = compare_text_values("Karnataka", "Kerala")
        self.assertFalse(res["match"])
        self.assertEqual(res["match_type"], "mismatch")

if __name__ == "__main__":
    unittest.main()
