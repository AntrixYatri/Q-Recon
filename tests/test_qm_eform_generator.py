import unittest
import os
import json
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
from ai_engine.synthetic_documents.qm_eform_generator import generate_qm_eform_image

class TestQMEFormGenerator(unittest.TestCase):
    def setUp(self):
        self.base_record = create_pmgsy_grounded_base_record(index=2, seed=42)
        self.output_dir = os.path.join(ROOT_DIR, "data", "synthetic")
        os.makedirs(self.output_dir, exist_ok=True)

    def test_generate_variant_a(self):
        img_path = os.path.join(self.output_dir, "qm_eform_var_a.png")
        sidecar_path = os.path.join(self.output_dir, "qm_eform_var_a.json")
        
        if os.path.exists(img_path):
            os.remove(img_path)
        if os.path.exists(sidecar_path):
            os.remove(sidecar_path)

        generate_qm_eform_image(self.base_record, img_path, variant="A", seed=42)
        
        self.assertTrue(os.path.exists(img_path))
        self.assertTrue(os.path.exists(sidecar_path))
        
        with open(sidecar_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            self.assertEqual(meta["variant"], "A")
            self.assertEqual(meta["seed"], 42)
            self.assertEqual(meta["provenance"]["data_origin"], "pmgsy_grounded_synthetic")

        # Cleanup
        os.remove(img_path)
        os.remove(sidecar_path)

    def test_generate_variant_b(self):
        img_path = os.path.join(self.output_dir, "qm_eform_var_b.png")
        sidecar_path = os.path.join(self.output_dir, "qm_eform_var_b.json")
        
        if os.path.exists(img_path):
            os.remove(img_path)
        if os.path.exists(sidecar_path):
            os.remove(sidecar_path)

        generate_qm_eform_image(self.base_record, img_path, variant="B", seed=42)
        
        self.assertTrue(os.path.exists(img_path))
        self.assertTrue(os.path.exists(sidecar_path))

        with open(sidecar_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            self.assertEqual(meta["variant"], "B")

        # Cleanup
        os.remove(img_path)
        os.remove(sidecar_path)

    def test_generate_variant_c(self):
        img_path = os.path.join(self.output_dir, "qm_eform_var_c.png")
        sidecar_path = os.path.join(self.output_dir, "qm_eform_var_c.json")
        
        if os.path.exists(img_path):
            os.remove(img_path)
        if os.path.exists(sidecar_path):
            os.remove(sidecar_path)

        generate_qm_eform_image(self.base_record, img_path, variant="C", seed=42)
        
        self.assertTrue(os.path.exists(img_path))
        self.assertTrue(os.path.exists(sidecar_path))

        with open(sidecar_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            self.assertEqual(meta["variant"], "C")

        # Cleanup
        os.remove(img_path)
        os.remove(sidecar_path)

if __name__ == "__main__":
    unittest.main()
