import copy
from ai_engine.testing.pmgsy_fixture_factory import generate_document_variants

def create_scenario(base_record: dict, scenario_type: str) -> list:
    """
    Mutates document variants from a PMGSY-grounded base record to produce a specific scenario.
    Returns a list of document inputs suitable for the analyze_documents pipeline.
    """
    variants = generate_document_variants(base_record)
    
    doc_qcr = copy.deepcopy(variants["QCR"])
    doc_td = copy.deepcopy(variants["TEST_DATASHEET"])
    doc_qm = copy.deepcopy(variants["QM_EFORM"])
    
    # Attach provenance to document metadata where the pipeline can read it
    doc_qcr["ocr_metadata"] = {"provenance": base_record.get("provenance")}
    doc_td["ocr_metadata"] = {"provenance": base_record.get("provenance")}
    doc_qm["ocr_metadata"] = {"provenance": base_record.get("provenance")}
    
    if scenario_type == "identical_documents":
        # All three documents are identical in values
        pass
        
    elif scenario_type == "formatting_difference":
        # e.g., "Karnataka" vs "karnataka "
        doc_qcr["fields"]["district"] = "Karnataka"
        doc_td["fields"]["district"] = "karnataka "
        doc_qm["fields"]["district"] = "KARNATAKA"
        
    elif scenario_type == "equivalent_units":
        # 150 mm vs 15 cm
        doc_qcr["fields"]["measured_value"] = "150"
        doc_qcr["fields"]["unit"] = "mm"
        
        doc_td["fields"]["measured_value"] = "15"
        doc_td["fields"]["unit"] = "cm"
        
        doc_qm["fields"]["measured_value"] = "150"
        doc_qm["fields"]["unit"] = "mm"
        
    elif scenario_type == "numerical_mismatch":
        # 150 mm vs 120 mm
        doc_qcr["fields"]["measured_value"] = "150"
        doc_qcr["fields"]["unit"] = "mm"
        
        doc_td["fields"]["measured_value"] = "120"
        doc_td["fields"]["unit"] = "mm"
        
        doc_qm["fields"]["measured_value"] = "150"
        doc_qm["fields"]["unit"] = "mm"
        
    elif scenario_type == "missing_value":
        # A configured field exists in some but is missing in another
        if "parameter" in doc_qm["fields"]:
            del doc_qm["fields"]["parameter"]
            
    elif scenario_type == "date_format_difference":
        # 12 Aug 2026 vs 2026-08-12
        doc_qcr["fields"]["inspection_date"] = "12 Aug 2026"
        doc_td["fields"]["inspection_date"] = "2026-08-12"
        doc_qm["fields"]["inspection_date"] = "12/08/2026"
        
    elif scenario_type == "actual_date_mismatch":
        # Different dates entirely
        doc_qcr["fields"]["inspection_date"] = "2026-08-12"
        doc_td["fields"]["inspection_date"] = "2026-08-19"
        doc_qm["fields"]["inspection_date"] = "2026-08-12"
        
    elif scenario_type == "majority_consensus":
        # 3 documents: 150, 150, 120
        doc_qcr["fields"]["measured_value"] = "150"
        doc_qcr["fields"]["unit"] = "mm"
        
        doc_td["fields"]["measured_value"] = "120"
        doc_td["fields"]["unit"] = "mm"
        
        doc_qm["fields"]["measured_value"] = "150"
        doc_qm["fields"]["unit"] = "mm"
        
    elif scenario_type == "ambiguous_conflict":
        # 2 documents disagreeing (1 vs 1)
        doc_qcr["fields"]["measured_value"] = "150"
        doc_qcr["fields"]["unit"] = "mm"
        
        doc_td["fields"]["measured_value"] = "120"
        doc_td["fields"]["unit"] = "mm"
        
        # We only return 2 documents for this scenario to create a 1v1 tie
        return [doc_qcr, doc_td]
        
    else:
        raise ValueError(f"Unknown scenario type: {scenario_type}")
        
    return [doc_qcr, doc_td, doc_qm]
