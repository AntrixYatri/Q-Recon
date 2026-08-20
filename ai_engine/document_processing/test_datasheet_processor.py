from ai_engine.document_processing.base_extractor import BaseDocumentExtractor

class TestDatasheetProcessor(BaseDocumentExtractor):
    """
    Test Datasheet Extractor scaffolding. Returns not_implemented for raw OCR
    but routes structured inputs successfully.
    """
    def extract(self, document_path_or_dict) -> dict:
        # Structured input bypass (Task 5)
        if isinstance(document_path_or_dict, dict):
            fields = document_path_or_dict.get("fields", {})
            return {
                "document_id": document_path_or_dict.get("document_id", "test_datasheet_doc"),
                "document_type": "TEST_DATASHEET",
                "classification_confidence": 1.0,
                "processing_status": "success",
                "extracted_fields": fields,
                "field_confidence": {k: 1.0 for k in fields.keys()},
                "metadata": {"source": "structured_input_bypass"}
            }
            
        # Raw document path (Task 5)
        return {
            "document_id": "test_datasheet_doc",
            "document_type": "TEST_DATASHEET",
            "classification_confidence": 1.0,
            "processing_status": "not_implemented",
            "extracted_fields": {},
            "field_confidence": {},
            "metadata": {
                "reason": "Raw Test Datasheet OCR extraction is not implemented yet."
            }
        }
