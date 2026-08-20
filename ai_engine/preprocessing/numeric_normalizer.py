import re
from decimal import Decimal, InvalidOperation

def parse_numeric_value(raw_val) -> Decimal:
    """
    Safely parses an input parameter string or number into a standard Decimal representation.
    Handles space trimming, comma decimals (e.g. 150,0 -> 150.0), and trailing unit symbols.
    """
    if raw_val is None:
        return None
        
    if isinstance(raw_val, (int, float)):
        return Decimal(str(raw_val))
        
    if isinstance(raw_val, Decimal):
        return raw_val

    # Normalize to string and clean
    text = str(raw_val).strip()
    
    # Extract first sequence of digits, decimal dots, or hyphens (for negatives)
    # E.g. '150 mm' -> '150', '150,0' -> '150.0', ' deficit 30.5' -> '30.5'
    text = text.replace(",", ".")
    match = re.search(r"(-?[0-9]+(?:\.[0-9]+)?)", text)
    if not match:
        return None
        
    try:
        return Decimal(match.group(1))
    except (InvalidOperation, ValueError):
        return None
