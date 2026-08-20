import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.discrepancy_engine.missing_value_checker import check_missing_values

class TestMissingValueChecker(unittest.TestCase):
    def test_missing_discrepancy(self):
        # field 'measured_value' has check_missing = True in config
        res = check_missing_values("150", None, "measured_value")
        self.assertTrue(res["discrepancy"])
        self.assertEqual(res["missing_in"], "document_b")

    def test_no_missing_discrepancy_when_both_present(self):
        res = check_missing_values("150", "150", "measured_value")
        self.assertFalse(res["discrepancy"])

    def test_no_missing_discrepancy_unconfigured_field(self):
        # field 'village' is config check_missing = False
        res = check_missing_values("Village A", None, "village")
        self.assertFalse(res["discrepancy"])

if __name__ == "__main__":
    unittest.main()
