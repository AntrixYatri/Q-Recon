from ai_engine.data_integration.canonical_schema import CanonicalRecord

def adapt_qcr_data(extracted_fields: dict, document_id: str, ocr_metadata: dict = None) -> CanonicalRecord:
    """
    Adapts extracted QCR dictionary fields from the OCR pipeline into a CanonicalRecord.
    """
    ocr_metadata = ocr_metadata or {}
    avg_ocr_conf = ocr_metadata.get("ocr_confidence")
    if avg_ocr_conf is not None:
        avg_ocr_conf = float(avg_ocr_conf) / 100.0 if avg_ocr_conf > 1.0 else float(avg_ocr_conf)

    record = CanonicalRecord()
    
    # Static doc info
    record.set_field("document_id", document_id, "QCR", "document_id")
    record.set_field("document_type", "QCR", "QCR", "document_type")
    
    if "source_file" in extracted_fields:
        record.set_field("source_file", extracted_fields["source_file"], "QCR", "source_file")

    # Map variables
    for field, val in extracted_fields.items():
        if val is None:
            continue
        
        # Check if field name is defined in schema
        if field in record.fields:
            record.set_field(
                field_name=field,
                value=val,
                source_document="QCR",
                source_field=field,
                ocr_confidence=avg_ocr_conf
            )
            
    return record

def adapt_test_datasheet_data(raw_data: dict, document_id: str, ocr_metadata: dict = None) -> CanonicalRecord:
    """
    Adapts demo or pre-extracted Test Datasheet dictionary parameters into a CanonicalRecord.
    """
    ocr_metadata = ocr_metadata or {}
    avg_ocr_conf = ocr_metadata.get("ocr_confidence")
    if avg_ocr_conf is not None:
        avg_ocr_conf = float(avg_ocr_conf) / 100.0 if avg_ocr_conf > 1.0 else float(avg_ocr_conf)

    record = CanonicalRecord()
    record.set_field("document_id", document_id, "TEST_DATASHEET", "document_id")
    record.set_field("document_type", "TEST_DATASHEET", "TEST_DATASHEET", "document_type")
    
    for field, val in raw_data.items():
        if val is None:
            continue
        
        # We will map standard names directly, or rely on schema_normalizer later.
        # But here we write the direct value map.
        if field in record.fields:
            record.set_field(
                field_name=field,
                value=val,
                source_document="TEST_DATASHEET",
                source_field=field,
                ocr_confidence=avg_ocr_conf
            )
    return record

def adapt_qm_eform_data(raw_data: dict, document_id: str, ocr_metadata: dict = None) -> CanonicalRecord:
    """
    Adapts demo or pre-extracted National Quality Monitor (NQM) E-Form parameters into a CanonicalRecord.
    """
    ocr_metadata = ocr_metadata or {}
    avg_ocr_conf = ocr_metadata.get("ocr_confidence")
    if avg_ocr_conf is not None:
        avg_ocr_conf = float(avg_ocr_conf) / 100.0 if avg_ocr_conf > 1.0 else float(avg_ocr_conf)

    record = CanonicalRecord()
    record.set_field("document_id", document_id, "QM_EFORM", "document_id")
    record.set_field("document_type", "QM_EFORM", "QM_EFORM", "document_type")
    
    for field, val in raw_data.items():
        if val is None:
            continue
        if field in record.fields:
            record.set_field(
                field_name=field,
                value=val,
                source_document="QM_EFORM",
                source_field=field,
                ocr_confidence=avg_ocr_conf
            )
    return record

def adapt_document(document_type: str, raw_data: dict, document_id: str, ocr_metadata: dict = None) -> CanonicalRecord:
    """
    Unified entrypoint adapter routing raw dictionaries based on document_type.
    """
    doc_type_upper = str(document_type).upper().strip()
    if doc_type_upper == "QCR":
        return adapt_qcr_data(raw_data, document_id, ocr_metadata)
    elif doc_type_upper == "TEST_DATASHEET":
        return adapt_test_datasheet_data(raw_data, document_id, ocr_metadata)
    elif doc_type_upper == "QM_EFORM":
        return adapt_qm_eform_data(raw_data, document_id, ocr_metadata)
    else:
        # Fallback adapter that maps any field matches
        record = CanonicalRecord()
        record.set_field("document_id", document_id, document_type, "document_id")
        record.set_field("document_type", document_type, document_type, "document_type")
        for k, v in raw_data.items():
            if k in record.fields:
                record.set_field(k, v, document_type, k)
        return record
