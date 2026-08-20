import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.preprocessing.numeric_normalizer import parse_numeric_value
from decimal import Decimal

class TestNumericNormalization(unittest.TestCase):
    def test_float_and_int(self):
        self.assertEqual(parse_numeric_value(150), Decimal("150"))
        self.assertEqual(parse_numeric_value(12.5), Decimal("12.5"))

    def test_string_decimals(self):
        self.assertEqual(parse_numeric_value("150.0"), Decimal("150.0"))
        self.assertEqual(parse_numeric_value(" 150 "), Decimal("150"))
        # Comma decimals
        self.assertEqual(parse_numeric_value("150,5"), Decimal("150.5"))
        # With units
        self.assertEqual(parse_numeric_value("120 mm"), Decimal("120"))

    def test_invalid_strings(self):
        self.assertIsNone(parse_numeric_value("abc"))
        self.assertIsNone(parse_numeric_value(""))

if __name__ == "__main__":
    unittest.main()
