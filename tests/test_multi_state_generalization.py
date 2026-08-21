import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.pipeline import analyze_documents
from ai_engine.document_processing.document_classifier import classify_document

class TestMultiStateGeneralization(unittest.TestCase):
    def test_multi_state_matrix(self):
        # 1. Classification
        res_ka = classify_document("", ocr_text="quality control register state karnataka pmgsy report")
        res_mh = classify_document("", ocr_text="quality control register state maharashtra pmgsy report")
        res_tn = classify_document("", ocr_text="quality control register state tamil nadu pmgsy report")
        
        self.assertEqual(res_ka["document_type"], "QCR")
        self.assertEqual(res_mh["document_type"], "QCR")
        self.assertEqual(res_tn["document_type"], "QCR")

        # 2. Pipeline Extraction, Normalization & Linking
        # Karnataka
        doc_ka_qcr = {
            "document_id": "KA-QCR",
            "document_type": "QCR",
            "fields": {
                "project_code": "PRJ-SOUTH-KA",
                "state": "Karnataka",
                "district": "Mysore",
                "measured_value": "150 mm",
                "required_value": "150 mm",
                "unit": "mm",
                "quality_status": "COMPLIANT"
            }
        }
        doc_ka_td = {
            "document_id": "KA-TD",
            "document_type": "TEST_DATASHEET",
            "fields": {
                "project_code": "PRJ-SOUTH-KA",
                "state": "karnataka",
                "district": "mysore",
                "measured_value": "15", # 15 cm = 150 mm
                "required_value": "15",
                "unit": "cm",
                "quality_status": "compliant"
            }
        }

        # Maharashtra
        doc_mh_qcr = {
            "document_id": "MH-QCR",
            "document_type": "QCR",
            "fields": {
                "project_code": "PRJ-WEST-MH",
                "state": "Maharashtra",
                "district": "Nagpur",
                "measured_value": "150 mm",
                "required_value": "150 mm",
                "unit": "mm",
                "quality_status": "pass"
            }
        }
        doc_mh_td = {
            "document_id": "MH-TD",
            "document_type": "TEST_DATASHEET",
            "fields": {
                "project_code": "PRJ-WEST-MH",
                "state": "maharashtra",
                "district": "nagpur",
                "measured_value": "15",
                "required_value": "15",
                "unit": "cm",
                "quality_status": "pass"
            }
        }

        # Tamil Nadu
        doc_tn_qcr = {
            "document_id": "TN-QCR",
            "document_type": "QCR",
            "fields": {
                "project_code": "PRJ-SOUTH-TN",
                "state": "Tamil Nadu",
                "district": "Chennai",
                "measured_value": "150 mm",
                "required_value": "150 mm",
                "unit": "mm",
                "quality_status": "approved"
            }
        }
        doc_tn_td = {
            "document_id": "TN-TD",
            "document_type": "TEST_DATASHEET",
            "fields": {
                "project_code": "PRJ-SOUTH-TN",
                "state": "tamil nadu",
                "district": "chennai",
                "measured_value": "15",
                "required_value": "15",
                "unit": "cm",
                "quality_status": "approved"
            }
        }

        # Batch analyze all documents together
        batch = [doc_ka_qcr, doc_ka_td, doc_mh_qcr, doc_mh_td, doc_tn_qcr, doc_tn_td]
        res = analyze_documents(batch)
        
        self.assertEqual(res["processing_status"], "success")
        self.assertEqual(res["documents_analyzed"], 6)

        # Directly verify record groups separation
        from ai_engine.data_integration.record_linker import group_records
        from ai_engine.data_integration.unified_data_builder import build_canonical_record
        records = [
            build_canonical_record(doc["document_id"], doc["document_type"], doc["fields"])
            for doc in batch
        ]
        groups = group_records(records)
        self.assertEqual(len(groups), 3)

        # There should be 0 discrepancies as the values inside each group are consistent (normalized & matched correctly)
        self.assertEqual(res["summary"]["total_discrepancies"], 0)

if __name__ == "__main__":
    unittest.main()
