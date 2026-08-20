from collections import Counter
from ai_engine.discrepancy_engine.comparison_config import COMPARISON_CONFIG
from ai_engine.discrepancy_engine.numerical_comparator import compare_numerical_values
from ai_engine.discrepancy_engine.text_comparator import compare_text_values
from ai_engine.discrepancy_engine.date_comparator import compare_date_values
from ai_engine.discrepancy_engine.missing_value_checker import check_missing_values

def analyze_field_across_records(field_name: str, records: list) -> list:
    """
    Compares field values across multiple documents in a linked project group.
    Uses majority consensus, authoritative source config lookup, and resolves
    1 vs 1 ties as ambiguous conflicts.
    """
    discrepancies = []
    
    field_cfg = COMPARISON_CONFIG.get(field_name)
    if not field_cfg:
        return []

    comp_type = field_cfg.get("comparison_type")
    
    # 1. Gather values and document references
    populated_docs = [] # list of (doc_id, doc_type, raw_val, canonical_val_obj)
    missing_docs = [] # list of (doc_id, doc_type)

    for rec in records:
        doc_id = rec.get_value("document_id") or "unknown_id"
        doc_type = rec.get_value("document_type")
        val_obj = rec.fields.get(field_name)
        val = val_obj.value if val_obj else None

        if (not doc_type or doc_type == "unknown_type") and val_obj and val_obj.source_document:
            doc_type = val_obj.source_document
        if not doc_type:
            doc_type = "unknown_type"

        if val is not None and str(val).strip() != "":
            populated_docs.append((doc_id, doc_type, val, val_obj))
        else:
            missing_docs.append((doc_id, doc_type))

    # 2. Check missing values if configured
    if field_cfg.get("check_missing", False) and missing_docs and populated_docs:
        for m_doc_id, m_doc_type in missing_docs:
            discrepancies.append({
                "field": field_name,
                "discrepancy_type": "missing_value",
                "comparison_status": "missing",
                "severity": "HIGH" if field_cfg.get("importance") == "high" else "MEDIUM",
                "explanation": (
                    f"Required field '{field_name}' is missing in {m_doc_type} ({m_doc_id}), "
                    f"but is populated in other linked documents."
                ),
                "documents": [
                    {
                        "document_id": m_doc_id,
                        "document_type": m_doc_type,
                        "value": None
                    }
                ],
                "values": [None],
                "normalized_values": [None],
                "difference": None,
                "percentage_difference": None,
                "metadata": {}
            })

    if len(populated_docs) < 2:
        return discrepancies # Not enough values to compare

    # 3. Compare values and cluster them
    value_clusters = [] # list of lists of populated_docs items

    for doc_item in populated_docs:
        _, _, val, _ = doc_item
        placed = False
        
        for cluster in value_clusters:
            repr_doc = cluster[0]
            _, _, repr_val, _ = repr_doc
            
            # Compare using type-specific comparators
            match = False
            if comp_type == "numeric":
                res = compare_numerical_values(val, repr_val, tolerance=field_cfg.get("tolerance", 0.01))
                match = res["match"]
            elif comp_type == "date":
                res = compare_date_values(val, repr_val)
                match = res["match"]
            else:
                res = compare_text_values(val, repr_val, field_name=field_name)
                match = res["match"]

            if match:
                cluster.append(doc_item)
                placed = True
                break

        if not placed:
            value_clusters.append([doc_item])

    # If there is only 1 value cluster, all values match!
    if len(value_clusters) <= 1:
        return discrepancies

    # 4. Configurable Consensus Resolution Logic
    # Sort clusters by size descending to check majority/ties
    value_clusters.sort(key=len, reverse=True)
    
    consensus_cluster = None
    is_ambiguous = False
    
    # Check if there is a majority cluster (size strictly greater than second largest)
    if len(value_clusters) == 1:
        consensus_cluster = value_clusters[0]
    elif len(value_clusters[0]) > len(value_clusters[1]):
        consensus_cluster = value_clusters[0]
    else:
        # A tie exists! Look up if there is a configured authoritative source type
        auth_type = field_cfg.get("authoritative_source")
        if auth_type:
            matching_auth_clusters = []
            for cluster in value_clusters:
                # Check if this cluster contains the authoritative source document type
                if any(item[1] == auth_type for item in cluster):
                    matching_auth_clusters.append(cluster)
            
            # If exactly one cluster contains the authority document type, it wins the tie!
            if len(matching_auth_clusters) == 1:
                consensus_cluster = matching_auth_clusters[0]
                # Re-sort to put consensus first
                value_clusters.remove(consensus_cluster)
                value_clusters.insert(0, consensus_cluster)
            else:
                is_ambiguous = True
        else:
            is_ambiguous = True

    # 5. Handle Ambiguous Conflict (Tie with no majority or authority)
    if is_ambiguous:
        involved_docs = []
        all_values = []
        all_norm_values = []
        values_by_doc = {}
        
        for cluster in value_clusters:
            repr_val = cluster[0][2]
            doc_ids = [item[0] for item in cluster]
            for item in cluster:
                all_values.append(str(item[2]))
                all_norm_values.append(str(item[2]))
                involved_docs.append({
                    "document_id": item[0],
                    "document_type": item[1],
                    "value": str(item[2]),
                    "normalized_value": str(item[2]),
                    "ocr_confidence": item[3].ocr_confidence
                })
            values_by_doc[str(repr_val)] = doc_ids

        explanation = (
            f"Ambiguous conflict on '{field_name}': The documents contain conflicting values "
            f"({', '.join(values_by_doc.keys())}), but no majority or authoritative source is available "
            f"to establish the correct value."
        )

        discrepancies.append({
            "field": field_name,
            "discrepancy_type": "ambiguous_conflict",
            "comparison_status": "ambiguous",
            "explanation": explanation,
            "documents": involved_docs,
            "values": all_values,
            "normalized_values": all_norm_values,
            "difference": None,
            "percentage_difference": None,
            "severity": "HIGH" if field_cfg.get("importance") == "high" else "MEDIUM",
            "confidence": 0.75, # Standard tie confidence reduction
            "metadata": {
                "consensus_found": False,
                "values": values_by_doc,
                "reason": "No majority or deterministic authoritative source exists."
            }
        })
        return discrepancies

    # 6. Handle Mismatch Outliers (Majority consensus exists)
    consensus_repr = consensus_cluster[0]
    _, _, consensus_val, _ = consensus_repr
    outlier_clusters = value_clusters[1:]

    for outlier_cluster in outlier_clusters:
        outlier_repr = outlier_cluster[0]
        o_doc_id, o_doc_type, o_val, o_val_obj = outlier_repr
        
        doc_names = ", ".join(f"{item[1]} ({item[0]})" for item in consensus_cluster)
        
        # Determine mismatch type and details
        if comp_type == "numeric":
            d_type = "numerical_mismatch"
            diff_res = compare_numerical_values(o_val, consensus_val)
            pct = diff_res.get("percentage_difference", 0.0)
            diff = diff_res.get("difference", 0.0)
            explanation = (
                f"Numerical mismatch on '{field_name}': {o_doc_type} ({o_doc_id}) reports '{o_val}', "
                f"which differs from the consensus value '{consensus_val}' found in {doc_names} "
                f"by {diff} ({pct:.1f}% difference)."
            )
        elif comp_type == "date":
            d_type = "date_mismatch"
            diff_res = compare_date_values(o_val, consensus_val)
            days = diff_res.get("days_difference", 0)
            explanation = (
                f"Date mismatch on '{field_name}': {o_doc_type} ({o_doc_id}) reports '{o_val}', "
                f"which differs from the consensus date '{consensus_val}' found in {doc_names} "
                f"by {days} days."
            )
        else:
            d_type = "text_mismatch"
            explanation = (
                f"Text mismatch on '{field_name}': {o_doc_type} ({o_doc_id}) reports '{o_val}', "
                f"which disagrees with the consensus value '{consensus_val}' found in {doc_names}."
            )

        # Build list of all involved document states
        involved_docs = []
        all_values = []
        all_norm_values = []
        for cluster in value_clusters:
            for item in cluster:
                all_values.append(str(item[2]))
                all_norm_values.append(str(item[2]))
                involved_docs.append({
                    "document_id": item[0],
                    "document_type": item[1],
                    "value": str(item[2]),
                    "normalized_value": str(item[2]),
                    "ocr_confidence": item[3].ocr_confidence
                })

        discrepancies.append({
            "field": field_name,
            "discrepancy_type": d_type,
            "comparison_status": "mismatch",
            "severity": "PENDING", # Calculated in scoring phase
            "confidence": "PENDING", # Calculated in scoring phase
            "explanation": explanation,
            "documents": involved_docs,
            "values": all_values,
            "normalized_values": all_norm_values,
            "difference": diff if comp_type == "numeric" else None,
            "percentage_difference": pct if comp_type == "numeric" else None,
            "metadata": {
                "consensus_found": True,
                "consensus_value": str(consensus_val)
            }
        })

    return discrepancies
