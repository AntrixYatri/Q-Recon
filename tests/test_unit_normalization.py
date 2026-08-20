import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.preprocessing.unit_normalizer import normalize_unit_value
from decimal import Decimal

class TestUnitNormalization(unittest.TestCase):
    def test_length_conversions(self):
        # 15 cm -> 150 mm
        res = normalize_unit_value("15 cm")
        self.assertTrue(res["success"])
        self.assertEqual(res["numeric_value"], Decimal("150"))
        self.assertEqual(res["normalized_unit"], "mm")

        # 1.5 m -> 1500 mm
        res = normalize_unit_value("1.5 m")
        self.assertTrue(res["success"])
        self.assertEqual(res["numeric_value"], Decimal("1500"))
        self.assertEqual(res["normalized_unit"], "mm")

    def test_mass_conversions(self):
        # 2 kg -> 2000 g
        res = normalize_unit_value("2 kg")
        self.assertTrue(res["success"])
        self.assertEqual(res["numeric_value"], Decimal("2000"))
        self.assertEqual(res["normalized_unit"], "g")

    def test_unsupported_or_no_units(self):
        # Plain number without unit should parse number, success is False because no unit string is recognized
        res = normalize_unit_value("150")
        self.assertEqual(res["numeric_value"], Decimal("150"))
        self.assertIsNone(res["normalized_unit"])

        # Unrecognized units (e.g. psi) are kept as-is
        res = normalize_unit_value("35 psi")
        self.assertEqual(res["numeric_value"], Decimal("35"))
        self.assertEqual(res["normalized_unit"], "psi")

if __name__ == "__main__":
    unittest.main()
