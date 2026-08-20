from datetime import datetime

def compare_date_values(date_str_a: str, date_str_b: str, tolerance_days: int = 0) -> dict:
    """
    Compares two date strings.
    If exact matching fails, calculates difference in days and compares against tolerance limits.
    """
    if not date_str_a or not date_str_b:
        return {
            "match": False,
            "error": "Missing input date",
            "reason": "One or both date strings are empty."
        }

    # Clean strings
    da = date_str_a.strip()
    db = date_str_b.strip()

    if da == db:
        return {
            "match": True,
            "days_difference": 0,
            "reason": "Dates are identical."
        }

    # Attempt to parse
    try:
        dt_a = datetime.strptime(da, "%Y-%m-%d")
        dt_b = datetime.strptime(db, "%Y-%m-%d")
    except ValueError:
        return {
            "match": False,
            "error": "Format parsing error",
            "reason": f"Dates must be normalized to YYYY-MM-DD prior to comparison. Got {da} and {db}."
        }

    days_diff = abs((dt_a - dt_b).days)
    match = days_diff <= tolerance_days
    reason = (
        f"Dates are within tolerance limits ({days_diff} days difference)."
        if match
        else f"Dates represent different days (difference of {days_diff} days)."
    )

    return {
        "match": bool(match),
        "days_difference": days_diff,
        "reason": reason
    }
