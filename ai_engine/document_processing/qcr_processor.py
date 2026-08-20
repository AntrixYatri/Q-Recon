from ai_engine.document_processing.base_extractor import BaseDocumentExtractor
from ai_engine.pipeline import analyze_document as legacy_analyze_document

class QCRProcessor(BaseDocumentExtractor):
    """
    QCR Extractor wrapping the existing layout-aware OCR extraction pipeline.
    Supports structured bypass input for demo and GPU-less testing.
    """
    def extract(self, document_path_or_dict) -> dict:
        # Structured input bypass (Task 4)
        if isinstance(document_path_or_dict, dict):
            fields = document_path_or_dict.get("fields", {})
            return {
                "document_id": document_path_or_dict.get("document_id", "qcr_doc"),
                "document_type": "QCR",
                "classification_confidence": 1.0,
                "processing_status": "success",
                "extracted_fields": fields,
                "field_confidence": {k: 1.0 for k in fields.keys()},
                "metadata": {"source": "structured_input_bypass"}
            }

        # Raw document path
        try:
            res = legacy_analyze_document(document_path_or_dict)
            return {
                "document_id": res.get("document_id") or "qcr_doc",
                "document_type": "QCR",
                "classification_confidence": 1.0,
                "processing_status": "success" if res.get("processing_status") == "success" else "failed",
                "extracted_fields": res.get("extracted_fields", {}),
                "field_confidence": res.get("field_confidence", {}),
                "metadata": res.get("ocr_metadata", {})
            }
        except Exception as e:
            return {
                "document_id": "qcr_doc",
                "document_type": "QCR",
                "classification_confidence": 1.0,
                "processing_status": "failed",
                "extracted_fields": {},
                "field_confidence": {},
                "metadata": {"error": str(e)}
            }
