import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.document_processing.document_classifier import classify_document

class TestClassifierHardening(unittest.TestCase):
    def test_classify_qcr(self):
        text = "quality control register with state, road name, and progress reports"
        res = classify_document("", ocr_text=text)
        self.assertEqual(res["document_type"], "QCR")
        self.assertGreaterEqual(res["confidence"], 0.5)

    def test_classify_test_datasheet(self):
        text = "test datasheet containing material test and laboratory test report"
        res = classify_document("", ocr_text=text)
        self.assertEqual(res["document_type"], "TEST_DATASHEET")
        self.assertGreaterEqual(res["confidence"], 0.5)

    def test_classify_qm_eform(self):
        text = "national quality monitoring report and independent quality monitoring with observations"
        res = classify_document("", ocr_text=text)
        self.assertEqual(res["document_type"], "QM_EFORM")
        self.assertGreaterEqual(res["confidence"], 0.5)

    def test_classify_unknown(self):
        text = "random hello world text with no signals"
        res = classify_document("", ocr_text=text)
        self.assertEqual(res["document_type"], "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
