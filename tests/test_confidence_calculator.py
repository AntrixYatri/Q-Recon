import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.scoring.confidence_calculator import calculate_confidence

class TestConfidenceCalculator(unittest.TestCase):
    def test_high_confidence(self):
        disc = {
            "documents": [
                {"ocr_confidence": 0.95},
                {"ocr_confidence": 0.92}
            ]
        }
        res = calculate_confidence(disc)
        self.assertGreaterEqual(res["confidence_score"], 0.85)
        self.assertEqual(res["confidence_level"], "HIGH")

    def test_low_confidence_on_error(self):
        disc = {
            "error": "Failed parsing decimal",
            "documents": [
                {"ocr_confidence": 0.70}
            ]
        }
        res = calculate_confidence(disc)
        self.assertLess(res["confidence_score"], 0.70)
        self.assertEqual(res["confidence_level"], "LOW")

if __name__ == "__main__":
    unittest.main()
