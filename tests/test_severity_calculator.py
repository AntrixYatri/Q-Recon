import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.scoring.severity_calculator import calculate_severity

class TestSeverityCalculator(unittest.TestCase):
    def test_critical_numerical_mismatch(self):
        disc = {
            "field": "measured_value",
            "discrepancy_type": "numerical_mismatch",
            "documents": [
                {"value": "150"},
                {"value": "120"}  # 20% deviation
            ]
        }
        res = calculate_severity(disc)
        self.assertEqual(res["severity"], "CRITICAL")
        self.assertTrue(any("deviation" in r for r in res["reasons"]))

    def test_high_severity_missing_critical(self):
        disc = {
            "field": "road_name",
            "discrepancy_type": "missing_value"
        }
        res = calculate_severity(disc)
        self.assertEqual(res["severity"], "HIGH")

    def test_low_severity_minor_field(self):
        disc = {
            "field": "village",
            "discrepancy_type": "text_mismatch"
        }
        res = calculate_severity(disc)
        self.assertEqual(res["severity"], "LOW")

if __name__ == "__main__":
    unittest.main()
