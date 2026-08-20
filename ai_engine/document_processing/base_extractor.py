from abc import ABC, abstractmethod

class BaseDocumentExtractor(ABC):
    """
    Abstract base class for all document-specific OCR extraction processors.
    """
    
    @abstractmethod
    def extract(self, document_path: str) -> dict:
        """
        Executes layout-aware OCR extraction and returns a standardized result dictionary.
        
        Expected output structure:
        {
            "document_id": str,
            "document_type": str,
            "classification_confidence": float,
            "processing_status": str, # e.g. "success", "not_implemented", "failed"
            "extracted_fields": dict, # canonical field values
            "field_confidence": dict, # confidence scores per field
            "metadata": dict
        }
        """
        pass
