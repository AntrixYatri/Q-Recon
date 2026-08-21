import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.pipeline import analyze_documents

class TestMixedDocumentE2E(unittest.TestCase):
    def test_mixed_projects_separation(self):
        # Project A inputs (Consistent 150 mm)
        proj_a_qcr = {
            "document_id": "A-QCR",
            "document_type": "QCR",
            "fields": {
                "project_code": "PRJ-AAA",
                "road_name": "Road Alpha",
                "measured_value": "150 mm",
                "required_value": "150 mm",
                "unit": "mm"
            }
        }
        proj_a_td = {
            "document_id": "A-TD",
            "document_type": "TEST_DATASHEET",
            "fields": {
                "project_code": "PRJ-AAA",
                "road_name": "Road Alpha",
                "measured_value": "15",
                "required_value": "15",
                "unit": "cm"
            }
        }

        # Project B inputs (Mismatched measured values)
        proj_b_qcr = {
            "document_id": "B-QCR",
            "document_type": "QCR",
            "fields": {
                "project_code": "PRJ-BBB",
                "road_name": "Road Beta",
                "measured_value": "150 mm",
                "required_value": "150 mm",
                "unit": "mm"
            }
        }
        proj_b_td = {
            "document_id": "B-TD",
            "document_type": "TEST_DATASHEET",
            "fields": {
                "project_code": "PRJ-BBB",
                "road_name": "Road Beta",
                "measured_value": "12", # 12 cm = 120 mm (mismatch!)
                "required_value": "15",
                "unit": "cm"
            }
        }

        # Mixed input batch order
        batch = [proj_b_td, proj_a_qcr, proj_b_qcr, proj_a_td]

        res = analyze_documents(batch)
        self.assertEqual(res["processing_status"], "success")

        discs = res["discrepancies"]
        
        # We expect exactly 1 discrepancy on measured_value (for Project B only)
        # Because Project A has consistent values (15 cm == 150 mm)
        measured_discs = [d for d in discs if d["field"] == "measured_value"]
        self.assertEqual(len(measured_discs), 1)

        disc = measured_discs[0]
        # Verify the discrepancy points to Project B documents, not Project A
        doc_ids = [d["document_id"] for d in disc["documents"]]
        self.assertIn("B-TD", doc_ids)
        self.assertIn("B-QCR", doc_ids)
        self.assertNotIn("A-TD", doc_ids)
        self.assertNotIn("A-QCR", doc_ids)

if __name__ == "__main__":
    unittest.main()
