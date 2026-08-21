import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.data_integration.unified_data_builder import build_canonical_record
from ai_engine.pipeline import analyze_documents

class TestDuplicateDocuments(unittest.TestCase):
    def test_duplicate_filtering(self):
        # 1 QCR and 2 identical QM E-Forms
        rec_qcr = {
            "document_id": "qcr-1",
            "document_type": "QCR",
            "fields": {
                "project_code": "PRJ-999",
                "inspection_date": "2026-03-04"
            }
        }
        
        rec_qm_1 = {
            "document_id": "qm-1",
            "document_type": "QM_EFORM",
            "fields": {
                "project_code": "PRJ-999",
                "inspection_date": "2026-03-10"
            }
        }

        # Near-identical duplicate of qm-1 (different doc_id, but same fields)
        rec_qm_2 = {
            "document_id": "qm-2",
            "document_type": "QM_EFORM",
            "fields": {
                "project_code": "PRJ-999",
                "inspection_date": "2026-03-10"
            }
        }

        # If deduplication is active, it will filter out qm-2.
        # So we have 1 QCR (03-04) and 1 QM (03-10).
        # This is a 1 vs 1 conflict on a field with no authoritative source -> Ambiguous!
        res = analyze_documents([rec_qcr, rec_qm_1, rec_qm_2])
        self.assertEqual(res["processing_status"], "success")
        
        discs = res["discrepancies"]
        date_disc = [d for d in discs if d["field"] == "inspection_date"]
        self.assertEqual(len(date_disc), 1)
        
        # Verify it detected an ambiguous conflict (1 vs 1 tie), rather than a mismatch!
        self.assertEqual(date_disc[0]["discrepancy_type"], "ambiguous_conflict")

if __name__ == "__main__":
    unittest.main()
