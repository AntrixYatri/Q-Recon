from ai_engine.discrepancy_engine.comparison_config import COMPARISON_CONFIG

def check_missing_values(val_a, val_b, field_name: str) -> dict:
    """
    Checks if there is a missing value discrepancy between two fields.
    Only triggers when the field config has check_missing = True.
    """
    field_cfg = COMPARISON_CONFIG.get(field_name, {})
    check_missing = field_cfg.get("check_missing", False)
    
    if not check_missing:
        return {"discrepancy": False}

    has_a = val_a is not None and str(val_a).strip() != ""
    has_b = val_b is not None and str(val_b).strip() != ""

    if has_a and not has_b:
        return {
            "discrepancy": True,
            "missing_in": "document_b",
            "reason": f"Required field '{field_name}' is populated in Document A but missing in Document B."
        }
    elif not has_a and has_b:
        return {
            "discrepancy": True,
            "missing_in": "document_a",
            "reason": f"Required field '{field_name}' is missing in Document A but populated in Document B."
        }

    return {"discrepancy": False}
