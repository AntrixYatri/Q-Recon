import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.pipeline import analyze_documents

class TestMultiDocumentPipeline(unittest.TestCase):
    def test_multi_document_pipeline_workflow(self):
        # Case 8: Three-document disagreement (consensus checking)
        document_inputs = [
            {
                "document_id": "QCR-001",
                "document_type": "QCR",
                "fields": {
                    "project_code": "PRJ-2026-T3",
                    "road_name": "Karimnagar Bypass",
                    "measured_val": "150 mm", # aliases will be normalized
                    "unit": "mm"
                }
            },
            {
                "document_id": "TEST-001",
                "document_type": "TEST_DATASHEET",
                "fields": {
                    "project_code": "PRJ-2026-T3",
                    "road_name": "Karimnagar Bypass",
                    "measured_val": "120 mm", # Outlier (mismatch!)
                    "unit": "mm"
                }
            },
            {
                "document_id": "QM-001",
                "document_type": "QM_EFORM",
                "fields": {
                    "project_code": "PRJ-2026-T3",
                    "road_name": "Karimnagar Bypass",
                    "measured_val": "15 cm", # Equivalent unit -> 150 mm (Matches QCR!)
                    "unit": "cm"
                }
            }
        ]

        res = analyze_documents(document_inputs)
        self.assertEqual(res["processing_status"], "success")
        self.assertEqual(res["documents_analyzed"], 3)
        self.assertEqual(res["summary"]["total_discrepancies"], 1) # Only 1 discrepancy (the outlier TEST-001)

        disc = res["discrepancies"][0]
        self.assertEqual(disc["field"], "measured_value")
        self.assertEqual(disc["discrepancy_type"], "numerical_mismatch")

if __name__ == "__main__":
    unittest.main()
