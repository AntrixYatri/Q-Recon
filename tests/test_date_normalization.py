import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.preprocessing.date_normalizer import normalize_date_string

class TestDateNormalization(unittest.TestCase):
    def test_slash_and_dash_formats(self):
        self.assertEqual(normalize_date_string("12/08/2026"), "2026-08-12")
        self.assertEqual(normalize_date_string("12-08-2026"), "2026-08-12")
        self.assertEqual(normalize_date_string("2026-08-12"), "2026-08-12")
        self.assertEqual(normalize_date_string("2026/08/12"), "2026-08-12")

    def test_text_month_formats(self):
        self.assertEqual(normalize_date_string("12 Aug 2026"), "2026-08-12")
        self.assertEqual(normalize_date_string("12 August 2026"), "2026-08-12")
        self.assertEqual(normalize_date_string("Aug 12, 2026"), "2026-08-12")

    def test_invalid_dates(self):
        self.assertIsNone(normalize_date_string("invalid_date_text"))
        self.assertIsNone(normalize_date_string(""))

if __name__ == "__main__":
    unittest.main()
