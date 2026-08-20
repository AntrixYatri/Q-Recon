from ai_engine.document_processing.qcr_processor import QCRProcessor
from ai_engine.document_processing.test_datasheet_processor import TestDatasheetProcessor
from ai_engine.document_processing.qm_eform_processor import QMEFormProcessor

EXTRACTOR_REGISTRY = {
    "QCR": QCRProcessor,
    "TEST_DATASHEET": TestDatasheetProcessor,
    "QM_EFORM": QMEFormProcessor
}

def get_extractor(document_type: str):
    """
    Retrieves and instantiates the appropriate document processor (Task 7).
    Returns None if no extractor is registered for the document type.
    """
    processor_cls = EXTRACTOR_REGISTRY.get(document_type)
    if processor_cls:
        return processor_cls()
    return None
