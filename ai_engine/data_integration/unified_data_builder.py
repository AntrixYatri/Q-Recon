from ai_engine.data_integration.canonical_schema import CanonicalRecord
from ai_engine.data_integration.document_adapter import adapt_document
from ai_engine.preprocessing.schema_normalizer import normalize_field_name
from ai_engine.preprocessing.date_normalizer import normalize_date_string
from ai_engine.preprocessing.unit_normalizer import normalize_unit_value

def build_canonical_record(document_id: str, document_type: str, raw_fields: dict, ocr_metadata: dict = None) -> CanonicalRecord:
    """
    Translates raw document dictionaries into structured CanonicalRecords.
    Normalizes field names (aliases) and value formats (dates, units) while maintaining origin tracing.
    """
    # 1. Normalize raw dictionary keys using schema configuration
    normalized_keys_data = {}
    for k, v in raw_fields.items():
        canonical_key = normalize_field_name(k)
        normalized_keys_data[canonical_key] = v

    # 2. Convert to CanonicalRecord via adapters
    record = adapt_document(document_type, normalized_keys_data, document_id, ocr_metadata)

    # 3. Normalize values inside the CanonicalRecord
    # Normalize Date Fields
    if record.get_value("inspection_date"):
        orig_date = record.get_value("inspection_date")
        iso_date = normalize_date_string(orig_date)
        if iso_date:
            record.fields["inspection_date"].value = iso_date

    # Normalize Measured / Required Values & Units
    meas_val = record.get_value("measured_value")
    req_val = record.get_value("required_value")
    unit_val = record.get_value("unit")

    # If measured value contains both number and unit (e.g. "150 mm")
    if meas_val is not None:
        norm_res = normalize_unit_value(meas_val, default_unit=unit_val)
        if norm_res["success"]:
            record.fields["measured_value"].value = str(norm_res["numeric_value"])
            record.fields["unit"].value = norm_res["normalized_unit"]
            # Also propagate unit if empty
            if not unit_val and norm_res["normalized_unit"]:
                record.set_field("unit", norm_res["normalized_unit"], document_type, "unit")

    # If required value contains unit
    if req_val is not None:
        norm_res = normalize_unit_value(req_val, default_unit=unit_val)
        if norm_res["success"]:
            record.fields["required_value"].value = str(norm_res["numeric_value"])
            # In case required value unit was different, the unit gets standardized.

    return record

def build_canonical_dataset(documents: list) -> list:
    """
    Accepts a list of document input dictionaries:
    [
      {
         "document_id": "QCR-001",
         "document_type": "QCR",
         "fields": {...},
         "ocr_metadata": {...}
      }
    ]
    and returns a list of resolved CanonicalRecord objects.
    """
    canonical_records = []
    for doc in documents:
        doc_id = doc.get("document_id")
        doc_type = doc.get("document_type", "UNKNOWN")
        fields = doc.get("fields", {})
        ocr_meta = doc.get("ocr_metadata")
        
        record = build_canonical_record(doc_id, doc_type, fields, ocr_meta)
        canonical_records.append(record)
        
    return canonical_records
