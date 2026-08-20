import re
from decimal import Decimal, InvalidOperation

# Unit conversion configurations
# Format: {raw_unit_alias: (base_unit, conversion_multiplier)}
UNIT_GROUPS = {
    # Length (base: mm)
    "mm": ("mm", Decimal("1")),
    "cm": ("mm", Decimal("10")),
    "m": ("mm", Decimal("1000")),
    "km": ("mm", Decimal("1000000")),
    
    # Mass (base: g)
    "g": ("g", Decimal("1")),
    "kg": ("g", Decimal("1000")),
    "t": ("g", Decimal("1000000")),
    "tonne": ("g", Decimal("1000000")),
    
    # Percentage (base: %)
    "%": ("%", Decimal("1")),
    "percent": ("%", Decimal("1")),
    
    # Temperature (base: °C)
    "°c": ("°C", Decimal("1")),
    "c": ("°C", Decimal("1")),
    "celsius": ("°C", Decimal("1"))
}

def clean_unit_string(unit: str) -> str:
    """
    Cleans up raw unit string for mapping dictionary lookup.
    """
    if not unit:
        return ""
    unit = str(unit).strip().lower()
    # Remove symbols like degree if isolated, but keep °C
    if unit in ["°c", "celsius", "c"]:
        return "°c"
    # Remove dots or spaces
    unit = unit.replace(".", "")
    return unit

def normalize_unit_value(value_str: str, default_unit: str = None) -> dict:
    """
    Parses a string (e.g., '15 cm'), extracts the numeric portion and the unit,
    and converts compatible units to a unified base standard.
    
    Returns a dict:
    {
        "original_value": str,
        "numeric_value": Decimal or None,
        "normalized_unit": str or None,
        "success": bool
    }
    """
    if value_str is None:
        return {"original_value": "", "numeric_value": None, "normalized_unit": None, "success": False}

    orig = str(value_str).strip()
    
    # Match decimal digits (supports commas) followed by text units
    match = re.match(r"^\s*([0-9.,\-]+)\s*(.*)$", orig)
    if not match:
        return {"original_value": orig, "numeric_value": None, "normalized_unit": None, "success": False}

    num_part, unit_part = match.groups()
    
    # Standardize comma decimals
    num_part = num_part.replace(",", ".")
    
    try:
        numeric = Decimal(num_part)
    except (InvalidOperation, ValueError):
        return {"original_value": orig, "numeric_value": None, "normalized_unit": None, "success": False}

    # Determine unit
    unit_str = clean_unit_string(unit_part)
    if not unit_str and default_unit:
        unit_str = clean_unit_string(default_unit)

    if unit_str in UNIT_GROUPS:
        base_unit, multiplier = UNIT_GROUPS[unit_str]
        normalized_num = numeric * multiplier
        return {
            "original_value": orig,
            "numeric_value": normalized_num,
            "normalized_unit": base_unit,
            "success": True
        }
        
    # Unrecognized unit or no unit (just number)
    return {
        "original_value": orig,
        "numeric_value": numeric,
        "normalized_unit": unit_part.strip() if unit_part else (default_unit or None),
        "success": bool(unit_part.strip())
    }
