import unittest
import os
import sys
from PIL import Image, ImageFilter

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
from ai_engine.synthetic_documents.qm_eform_generator import generate_qm_eform_image
from ai_engine.pipeline import process_mixed_document
from ai_engine.document_processing.document_classifier import classify_document

class TestOcrRobustness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_record = create_pmgsy_grounded_base_record(index=20, seed=42)
        cls.base_record["measured_value"] = "150"
        cls.base_record["unit"] = "mm"
        cls.base_record["parameter"] = "Pavement Thickness"
        cls.base_record["required_value"] = "150"
        cls.base_record["quality_status"] = "COMPLIANT"

        cls.clean_path = os.path.join(ROOT_DIR, "data", "synthetic", "robustness_clean.png")
        cls.degraded_path = os.path.join(ROOT_DIR, "data", "synthetic", "robustness_degraded.png")

        # Generate clean image
        generate_qm_eform_image(cls.base_record, cls.clean_path, variant="B", seed=42)

        # Degrade the image (Blur + low JPEG quality)
        img = Image.open(cls.clean_path)
        blurred = img.filter(ImageFilter.GaussianBlur(radius=1.0))
        blurred.save(cls.degraded_path, "JPEG", quality=40)

        # Run OCR once on the degraded image and cache
        cls.classification_cached = classify_document(cls.degraded_path)
        cls.extraction_cached = process_mixed_document(cls.degraded_path)

    @classmethod
    def tearDownClass(cls):
        for path in [cls.clean_path, cls.degraded_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
            json_path = os.path.splitext(path)[0] + ".json"
            if os.path.exists(json_path):
                try:
                    os.remove(json_path)
                except Exception:
                    pass

    def test_degraded_classification(self):
        res = self.classification_cached
        # Classifier should be robust enough to classify even blurred form
        self.assertEqual(res["document_type"], "QM_EFORM")

    def test_degraded_extraction(self):
        res = self.extraction_cached
        self.assertEqual(res["processing_status"], "success")
        
        extracted = res["extracted_fields"]
        # Basic fields like parameter, unit, and required value should still match
        self.assertEqual(extracted.get("unit"), "mm")
        self.assertEqual(extracted.get("required_value"), "150")

if __name__ == "__main__":
    unittest.main()
