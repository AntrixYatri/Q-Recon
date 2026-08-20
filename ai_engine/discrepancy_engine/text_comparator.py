import difflib
from ai_engine.preprocessing.field_normalizer import normalize_field_value

def compare_text_values(val_a, val_b, field_name: str = None) -> dict:
    """
    Compares two text fields.
    Classifies comparison results into: 'exact_match', 'normalized_match', 'probable_match', or 'mismatch'.
    """
    str_a = str(val_a) if val_a is not None else ""
    str_b = str(val_b) if val_b is not None else ""

    # 1. Exact Match Check
    if str_a == str_b:
        return {
            "match": True,
            "match_type": "exact_match",
            "similarity": 1.0,
            "reason": "Strings are identical."
        }

    # 2. Normalized Match Check
    norm_a = normalize_field_value(field_name or "text", str_a)
    norm_b = normalize_field_value(field_name or "text", str_b)
    
    if norm_a == norm_b:
        return {
            "match": True,
            "match_type": "normalized_match",
            "similarity": 1.0,
            "reason": "Strings match after standard lowercase and whitespace normalisation."
        }

    # 3. Probable Match check (Sequence similarity threshold > 0.82)
    similarity = difflib.SequenceMatcher(None, norm_a, norm_b).ratio()
    if similarity >= 0.82:
        return {
            "match": True,
            "match_type": "probable_match",
            "similarity": round(similarity, 3),
            "reason": f"Strings show high similarity ({round(similarity*100)}%) indicating probable spelling variation."
        }

    # 4. Mismatch
    return {
        "match": False,
        "match_type": "mismatch",
        "similarity": round(similarity, 3),
        "reason": "Strings represent fundamentally different values."
    }

# Post-processing logic for text comparisons.
