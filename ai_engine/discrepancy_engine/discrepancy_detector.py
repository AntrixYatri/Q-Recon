import os
import json
from ai_engine.data_integration.canonical_schema import CanonicalRecord
from ai_engine.data_integration.record_linker import group_records
from ai_engine.discrepancy_engine.cross_document_checker import analyze_field_across_records
from ai_engine.discrepancy_engine.rule_engine import check_logical_rules
from ai_engine.scoring.severity_calculator import calculate_severity
from ai_engine.scoring.confidence_calculator import calculate_confidence
from ai_engine.config.settings import DATA_PROCESSED_DIR, DATA_SYNTHETIC_DIR

def detect_discrepancies(records: list) -> list:
    """
    Orchestrates comparison across a list of CanonicalRecords.
    Links records into project groups, runs consensus comparisons, 
    logical rules, and applies severity/confidence scoring.
    """
    discrepancies = []
    
    # 1. Group records by road project
    grouped_projects = group_records(records)

    for group in grouped_projects:
        group_id = group["group_id"]
        group_records_list = group["records"]

        # Track documents in group for provenance reference
        involved_docs = []
        for rec in group_records_list:
            involved_docs.append({
                "document_id": rec.get_value("document_id") or "unknown_id",
                "document_type": rec.get_value("document_type") or "unknown_type"
            })

        # 2. Run Cross-Document Field Level Checks (mismatches, missing values)
        # We check all canonical fields that have configurations defined
        from ai_engine.discrepancy_engine.comparison_config import COMPARISON_CONFIG
        for field in COMPARISON_CONFIG.keys():
            field_discrepancies = analyze_field_across_records(field, group_records_list)
            for disc in field_discrepancies:
                disc["group_id"] = group_id
                discrepancies.append(disc)

        # 3. Run Single-Record Logical Rules
        for rec in group_records_list:
            logical_discrepancies = check_logical_rules(rec)
            for disc in logical_discrepancies:
                # Add metadata
                doc_id = rec.get_value("document_id")
                doc_type = rec.get_value("document_type")
                disc["group_id"] = group_id
                disc["documents"] = [
                    {
                        "document_id": doc_id,
                        "document_type": doc_type,
                        "value": str(rec.get_value(disc["field"]))
                    }
                ]
                discrepancies.append(disc)

    # 4. Score and standardize all generated discrepancies
    standardized_discrepancies = []
    for disc in discrepancies:
        # Run severity calculator
        sev_res = calculate_severity(disc)
        disc["severity"] = sev_res["severity"]
        disc["severity_reasons"] = sev_res["reasons"]

        # Run confidence calculator
        conf_res = calculate_confidence(disc)
        disc["confidence"] = conf_res["confidence_score"]
        disc["confidence_level"] = conf_res["confidence_level"]
        disc["confidence_factors"] = conf_res["factors"]
        
        # Standardize structure matching Canonical Discrepancy Schema (Task 4) with unique UUID (Task 5)
        import uuid
        canonical = {
            "id": str(uuid.uuid4()),
            "field": disc.get("field"),
            "discrepancy_type": disc.get("discrepancy_type"),
            "documents": disc.get("documents", []),
            "values": disc.get("values", []),
            "normalized_values": disc.get("normalized_values", []),
            "comparison_status": disc.get("comparison_status", "mismatch"),
            "difference": disc.get("difference"),
            "percentage_difference": disc.get("percentage_difference"),
            "severity": disc.get("severity", "MEDIUM"),
            "severity_reasons": disc.get("severity_reasons", []),
            "confidence": disc.get("confidence", 1.0),
            "confidence_level": disc.get("confidence_level", "HIGH"),
            "confidence_factors": disc.get("confidence_factors", {}),
            "explanation": disc.get("explanation", ""),
            "group_id": disc.get("group_id", "GROUP-1"),
            "metadata": disc.get("metadata", {})
        }
        standardized_discrepancies.append(canonical)

    return standardized_discrepancies

def compare_documents(analysis_id: str) -> dict:
    """
    Loads documents associated with an analysis session,
    performs cross-document mapping, and returns a structured discrepancy audit log.
    """
    records = []

    # 1. Look for uploaded files locally in the processed folder
    session_dir = os.path.join(DATA_PROCESSED_DIR, analysis_id)
    if os.path.exists(session_dir):
        for filename in os.listdir(session_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(session_dir, filename), "r") as f:
                        data = json.load(f)
                        records.append(CanonicalRecord.from_dict(data))
                except Exception:
                    pass

    # 2. Demo path fallback: If no files exist, populate standard demo data 
    # covering numerical, text, missing value, and equivalent unit test cases
    if not records:
        print(f"[Discrepancy Detector] No records found for analysis_id {analysis_id}. Generating mock demo dataset.")
        records = get_demo_canonical_dataset()

    discrepancies = detect_discrepancies(records)

    # Return structured multi-document summary payload
    total_disc = len(discrepancies)
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for disc in discrepancies:
        sev = str(disc.get("severity", "MEDIUM")).upper()
        if sev in severity_counts:
            severity_counts[sev] += 1
            
    # Programmatic verification of consistency (Task 6)
    assert sum(severity_counts.values()) == total_disc, "Programmatic summary counts mismatch."

    return {
        "analysis_id": analysis_id,
        "processing_status": "success",
        "documents_analyzed": len(records),
        "linked_record_groups": len(set(disc.get("group_id", "GROUP-1") for disc in discrepancies)) if discrepancies else 1,
        "summary": {
            "total_discrepancies": total_disc,
            "critical": severity_counts["CRITICAL"],
            "high": severity_counts["HIGH"],
            "medium": severity_counts["MEDIUM"],
            "low": severity_counts["LOW"]
        },
        "discrepancies": discrepancies
    }

def get_demo_canonical_dataset() -> list:
    """
    Returns a rich, linked canonical dataset used for demo / testing.
    Uses the PMGSY grounded fixture factory to build these records deterministically.
    """
    from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record, generate_document_variants
    from ai_engine.data_integration.unified_data_builder import build_canonical_record
    
    # 1. Generate base record from PMGSY dataset row 0
    base_rec = create_pmgsy_grounded_base_record(0, seed=42)
    
    # Ensure standard values
    base_rec["measured_value"] = "150"
    base_rec["unit"] = "mm"
    base_rec["parameter"] = "Pavement Thickness"
    base_rec["required_value"] = "150"
    base_rec["quality_status"] = "COMPLIANT"
    
    # 2. Get document variants
    variants = generate_document_variants(base_rec)
    
    qcr_var = variants["QCR"]
    td_var = variants["TEST_DATASHEET"]
    qm_var = variants["QM_EFORM"]
    
    # Modify QCR document ID to match legacy
    qcr_var["document_id"] = "DEMO-QCR-01"
    
    # Modify Test Datasheet to have equivalent unit but numerical mismatch
    td_var["document_id"] = "DEMO-TEST-01"
    td_var["fields"]["measured_value"] = "12"
    td_var["fields"]["unit"] = "cm"
    td_var["fields"]["required_value"] = "15" # 15 cm = 150 mm
    
    # Modify QM E-Form to have missing parameter
    qm_var["document_id"] = "DEMO-QM-01"
    if "parameter" in qm_var["fields"]:
        del qm_var["fields"]["parameter"]
        
    # Build CanonicalRecords
    rec_qcr = build_canonical_record(qcr_var["document_id"], "QCR", qcr_var["fields"], {"provenance": qcr_var["provenance"]})
    rec_td = build_canonical_record(td_var["document_id"], "TEST_DATASHEET", td_var["fields"], {"provenance": td_var["provenance"]})
    rec_qm = build_canonical_record(qm_var["document_id"], "QM_EFORM", qm_var["fields"], {"provenance": qm_var["provenance"]})
    
    return [rec_qcr, rec_td, rec_qm]
