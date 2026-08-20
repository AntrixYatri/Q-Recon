def calculate_severity(discrepancy: dict) -> dict:
    """
    Computes a logical severity classification (LOW, MEDIUM, HIGH, CRITICAL)
    for a discrepancy based on field importance, difference metrics, and record weights.
    """
    field = discrepancy.get("field", "")
    disc_type = discrepancy.get("discrepancy_type", "")
    
    reasons = []
    
    # Base importance mapper
    from ai_engine.discrepancy_engine.comparison_config import COMPARISON_CONFIG
    field_cfg = COMPARISON_CONFIG.get(field, {})
    importance = field_cfg.get("importance", "medium")

    # 1. Critical cases: numerical mismatches on measured/required fields with large differences
    if disc_type == "numerical_mismatch" and field in ["measured_value", "required_value"]:
        reasons.append("Discrepancy affects structural test measurements.")
        
        # Calculate deviation percentage if available
        # Find involved documents and check difference
        involved_docs = discrepancy.get("documents", [])
        if len(involved_docs) >= 2:
            try:
                val_a = float(involved_docs[0].get("value"))
                val_b = float(involved_docs[1].get("value"))
                diff = abs(val_a - val_b)
                pct = (diff / val_a * 100) if val_a else 0.0
                
                if pct > 15.0:
                    reasons.append(f"Significant parameter deviation detected ({pct:.1f}% error is > 15% limit).")
                    return {"severity": "CRITICAL", "reasons": reasons}
                else:
                    reasons.append(f"Moderate parameter deviation detected ({pct:.1f}% error).")
                    return {"severity": "HIGH", "reasons": reasons}
            except (ValueError, TypeError):
                pass
        
        return {"severity": "HIGH", "reasons": reasons}

    # 2. High severity: missing critical information
    if disc_type == "missing_value" and importance == "high":
        reasons.append("Critical road safety or audit field is missing in one or more records.")
        return {"severity": "HIGH", "reasons": reasons}

    # 3. High severity: logical inconsistency in status reporting
    if disc_type == "logical_inconsistency":
        reasons.append("Logical conflict: Record declarations violate internal compliance rules.")
        return {"severity": "HIGH", "reasons": reasons}

    # 4. Medium severity: text mismatches on high importance fields
    if disc_type in ["text_mismatch", "date_mismatch"] and importance == "high":
        reasons.append(f"Important descriptive field '{field}' disagrees across records.")
        return {"severity": "HIGH" if disc_type == "date_mismatch" else "MEDIUM", "reasons": reasons}

    # 5. Low severity: text mismatches on low importance fields
    if importance == "low":
        reasons.append("Minor naming spelling variation on lower priority field.")
        return {"severity": "LOW", "reasons": reasons}

    # Default fallback
    reasons.append("Standard field mismatch of medium importance.")
    return {"severity": "MEDIUM", "reasons": reasons}
