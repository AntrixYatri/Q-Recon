import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.discrepancy_engine.numerical_comparator import compare_numerical_values

class TestNumericalComparison(unittest.TestCase):
    def test_exact_match(self):
        res = compare_numerical_values(150, 150.0)
        self.assertTrue(res["match"])
        self.assertEqual(res["difference"], 0.0)

    def test_tolerance_match(self):
        res = compare_numerical_values(150.005, 150.001, tolerance=0.01)
        self.assertTrue(res["match"])

    def test_mismatch_difference(self):
        res = compare_numerical_values(150, 120, tolerance=0.01)
        self.assertFalse(res["match"])
        self.assertEqual(res["difference"], 30.0)
        self.assertEqual(res["percentage_difference"], 20.0)

if __name__ == "__main__":
    unittest.main()
