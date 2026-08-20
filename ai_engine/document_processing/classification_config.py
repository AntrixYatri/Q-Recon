CLASSIFICATION_CONFIG = {
    # Minimum aggregate score required to classify a document type confidently (Task 3)
    "confidence_threshold": 0.50,
    
    # Document Type Labels
    "document_types": {
        "QCR": "QCR",
        "TEST_DATASHEET": "TEST_DATASHEET",
        "QM_EFORM": "QM_EFORM",
        "UNKNOWN": "UNKNOWN"
    },
    
    # Weighted keyword signals found in text (Task 2 & 3)
    "weighted_signals": {
        "QCR": {
            "quality control register": 0.6,
            "quality control report": 0.6,
            "inspection type": 0.3,
            "quality status": 0.3,
            "pavement thickness": 0.2,
            "measured value": 0.2
        },
        "TEST_DATASHEET": {
            "test datasheet": 0.6,
            "test result": 0.4,
            "material test": 0.4,
            "laboratory": 0.3,
            "core diameter": 0.2,
            "compressive strength": 0.2
        },
        "QM_EFORM": {
            "quality monitoring": 0.6,
            "qm e-form": 0.6,
            "monitoring inspection": 0.4,
            "e-form": 0.3,
            "independent inspection": 0.2
        }
    },
    
    # Filename match hints as a weak fallback (Task 3)
    "filename_hints": {
        "QCR": ["qcr", "register", "quality_control"],
        "TEST_DATASHEET": ["test", "datasheet", "sheet", "lab"],
        "QM_EFORM": ["qm", "eform", "monitoring"]
    }
}
