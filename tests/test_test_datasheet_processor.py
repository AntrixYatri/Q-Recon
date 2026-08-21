import unittest
from unittest.mock import patch, MagicMock
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.document_processing.test_datasheet_processor import TestDatasheetProcessor

class TestTestDatasheetProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TestDatasheetProcessor()
        self.output_dir = os.path.join(ROOT_DIR, "data", "synthetic")
        os.makedirs(self.output_dir, exist_ok=True)

    def test_missing_pymupdf_dependency_fallback(self):
        # 1. Test missing PyMuPDF dependency fallback (raises ImportError)
        # Patch sys.modules to raise ImportError when fitz is imported
        with patch.dict(sys.modules, {"fitz": None}):
            res = self.processor.extract("nonexistent_test.pdf")
            self.assertEqual(res["processing_status"], "unsupported")
            self.assertEqual(res["error_type"], "pdf_processing_unavailable")
            self.assertIn("requires PyMuPDF", res["message"])

    def test_corrupt_or_unreadable_pdf_handling(self):
        # 2. Test corrupt/invalid PDF file handling
        # Create a corrupt PDF file (dummy text instead of real PDF header)
        corrupt_pdf_path = os.path.join(self.output_dir, "corrupt_test.pdf")
        with open(corrupt_pdf_path, "w") as f:
            f.write("THIS IS NOT A VALID PDF FILE HEADER")

        try:
            res = self.processor.extract(corrupt_pdf_path)
            self.assertEqual(res["processing_status"], "failed")
            self.assertEqual(res["error_type"], "invalid_or_unreadable_pdf")
            self.assertIn("Failed to render PDF", res["message"])
        finally:
            if os.path.exists(corrupt_pdf_path):
                os.remove(corrupt_pdf_path)

    def test_regression_jpg_png_unaffected(self):
        # 3. Regression check ensuring PNG/JPG processing is unaffected
        # If we pass a nonexistent PNG, it raises FileNotFoundError (file_error) rather than PDF errors
        res = self.processor.extract("nonexistent_image.png")
        self.assertEqual(res["processing_status"], "failed")
        self.assertEqual(res["error_type"], "file_error")
        self.assertIn("does not exist", res["message"])

if __name__ == "__main__":
    unittest.main()
