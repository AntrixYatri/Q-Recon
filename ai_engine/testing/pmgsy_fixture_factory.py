import random
from ai_engine.data_generation.pmgsy_qcr_generator import generate_pmgsy_qcr_record
from ai_engine.testing.dataset_loader import select_deterministic_record
from ai_engine.testing.provenance import create_provenance_metadata
from ai_engine.data_integration.canonical_schema import CanonicalRecord
from ai_engine.data_integration.unified_data_builder import build_canonical_record

def create_pmgsy_grounded_base_record(index: int, seed: int = 42) -> dict:
    """
    Generates a deterministic PMGSY-grounded base record with attached provenance.
    The base road/project identity is sourced directly from the PMGSY dataset.
    """
    random_state = random.getstate()
    random.seed(seed)
    try:
        # Select row deterministically
        selection = select_deterministic_record(index)
        row = selection["row"]
        row_idx = selection["index"]
        
        # Generate raw record using the PMGSY generator
        base_rec = generate_pmgsy_qcr_record(index, row)
        
        # Ensure canonical road_name is populated and maps to facility_name
        base_rec["road_name"] = base_rec.get("facility_name", "")
        base_rec["project_name"] = f"PMGSY - {base_rec['facility_name']} Quality Project"
        base_rec["project_code"] = f"PRJ-PMGSY-{base_rec.get('habitation_id', '000000')}"
        base_rec["road_code"] = f"RD-PMGSY-{str(base_rec.get('habitation_id', '00000'))[-5:]}"
        base_rec["road_length"] = 4.2
        base_rec["road_category"] = "Rural Road"
        
        # Generate and attach provenance metadata based on actual row and seed used
        provenance = create_provenance_metadata(row_idx, base_rec["image_id"], seed)
        base_rec["provenance"] = provenance
        
        return base_rec
    finally:
        random.setstate(random_state)

def create_canonical_base_record(base_record: dict) -> CanonicalRecord:
    """
    Converts a base generated record dictionary to a CanonicalRecord,
    storing the provenance in the ocr_metadata.
    """
    fields = {k: v for k, v in base_record.items() if k != "provenance"}
    provenance = base_record.get("provenance", {})
    return build_canonical_record(
        document_id=base_record.get("image_id", "base_doc"),
        document_type="QCR",
        raw_fields=fields,
        ocr_metadata={"provenance": provenance}
    )

def generate_document_variants(base_record: dict) -> dict:
    """
    Generates consistent document-specific variants (QCR, Test Datasheet, QM E-Form)
    sharing the exact same project/road identity sourced from the PMGSY base record.
    """
    provenance = base_record.get("provenance")
    
    # QCR variant fields
    qcr_fields = base_record.copy()
    if "provenance" in qcr_fields:
        del qcr_fields["provenance"]
        
    # Test Datasheet variant fields
    td_fields = {
        "project_code": base_record.get("project_code"),
        "road_name": base_record.get("road_name"),
        "district": base_record.get("district"),
        "block": base_record.get("block"),
        "habitation_name": base_record.get("habitation_name"),
        "habitation_id": base_record.get("habitation_id"),
        "parameter": base_record.get("parameter"),
        "required_value": base_record.get("required_value"),
        "measured_value": base_record.get("measured_value"),
        "unit": base_record.get("unit"),
        "inspection_date": base_record.get("inspection_date"),
        "quality_status": base_record.get("quality_status")
    }
    
    # QM E-Form variant fields
    qm_fields = {
        "project_code": base_record.get("project_code"),
        "road_name": base_record.get("road_name"),
        "district": base_record.get("district"),
        "block": base_record.get("block"),
        "habitation_name": base_record.get("habitation_name"),
        "habitation_id": base_record.get("habitation_id"),
        "parameter": base_record.get("parameter"),
        "required_value": base_record.get("required_value"),
        "measured_value": base_record.get("measured_value"),
        "unit": base_record.get("unit"),
        "inspection_date": base_record.get("inspection_date"),
        "quality_status": base_record.get("quality_status")
    }
    
    return {
        "QCR": {
            "document_id": base_record["image_id"],
            "document_type": "QCR",
            "fields": qcr_fields,
            "provenance": provenance
        },
        "TEST_DATASHEET": {
            "document_id": base_record["image_id"].replace("qcr", "td").replace("pmgsy_qcr", "pmgsy_td"),
            "document_type": "TEST_DATASHEET",
            "fields": td_fields,
            "provenance": provenance
        },
        "QM_EFORM": {
            "document_id": base_record["image_id"].replace("qcr", "qm").replace("pmgsy_qcr", "pmgsy_qm"),
            "document_type": "QM_EFORM",
            "fields": qm_fields,
            "provenance": provenance
        }
    }
