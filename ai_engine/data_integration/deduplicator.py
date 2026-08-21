from ai_engine.data_integration.canonical_schema import CanonicalRecord
from ai_engine.preprocessing.field_normalizer import normalize_field_value

def deduplicate_records(records: list) -> list:
    """
    Identifies and removes duplicate documents in a session based on:
    - Same document type
    - Same project code / identity signals
    - Identical canonical parameter fields (measured_value, required_value, quality_status, inspection_date)
    Returns a deduplicated list of CanonicalRecord objects.
    """
    if not records:
        return []

    unique_records = []
    seen_fingerprints = set()

    for rec in records:
        doc_type = rec.get_value("document_type") or "unknown"
        
        # Normalize fields for fingerprinting
        p_code = normalize_field_value("project_code", rec.get_value("project_code"))
        meas_val = normalize_field_value("measured_value", rec.get_value("measured_value"))
        req_val = normalize_field_value("required_value", rec.get_value("required_value"))
        status = normalize_field_value("quality_status", rec.get_value("quality_status"))
        date = normalize_field_value("inspection_date", rec.get_value("inspection_date"))
        
        # Fingerprint tuple
        fingerprint = (
            doc_type.lower(),
            p_code,
            meas_val,
            req_val,
            status,
            date
        )

        if fingerprint not in seen_fingerprints:
            seen_fingerprints.add(fingerprint)
            unique_records.append(rec)
        else:
            print(f"[Deduplicator Info] Skipped duplicate document '{rec.get_value('document_id')}' of type '{doc_type}'")

    return unique_records
