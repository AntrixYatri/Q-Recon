from decimal import Decimal

def compare_numerical_values(val_a, val_b, tolerance: float = 0.01) -> dict:
    """
    Compares two numerical values using Decimal for float-safety.
    Supports tolerance thresholds and calculates absolute and percentage differences.
    """
    if val_a is None or val_b is None:
        return {
            "match": False,
            "error": "Missing input value",
            "reason": "One or both numerical comparison values are null."
        }

    try:
        dec_a = Decimal(str(val_a))
        dec_b = Decimal(str(val_b))
    except Exception as e:
        return {
            "match": False,
            "error": "Parsing failure",
            "reason": f"Failed to parse inputs to Decimal: {str(e)}"
        }

    difference = abs(dec_a - dec_b)
    
    # Avoid division by zero
    if dec_a != 0:
        pct_diff = (difference / abs(dec_a)) * Decimal("100")
    elif dec_b != 0:
        pct_diff = (difference / abs(dec_b)) * Decimal("100")
    else:
        pct_diff = Decimal("0")

    tol_decimal = Decimal(str(tolerance))
    match = difference <= tol_decimal

    reason = "Values are within tolerance limits" if match else "Difference exceeds configured tolerance"

    return {
        "match": bool(match),
        "value_a": float(dec_a),
        "value_b": float(dec_b),
        "difference": float(difference),
        "percentage_difference": float(pct_diff),
        "reason": reason
    }
