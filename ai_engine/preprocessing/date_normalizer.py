import re
from datetime import datetime

DATE_FORMATS = [
    "%Y-%m-%d",      # 2026-08-12
    "%d/%m/%Y",      # 12/08/2026
    "%d-%m-%Y",      # 12-08-2026
    "%Y/%m/%d",      # 2026/08/12
    "%d %b %Y",      # 12 Aug 2026
    "%d %B %Y",      # 12 August 2026
    "%b %d, %Y",     # Aug 12, 2026
    "%B %d, %Y"      # August 12, 2026
]

def normalize_date_string(raw_date) -> str:
    """
    Standardises date text formats to ISO YYYY-MM-DD.
    If parsing fails, returns None (does not hallucinate).
    """
    if raw_date is None:
        return None
        
    date_str = str(raw_date).strip()
    if not date_str:
        return None

    # Replace multiple spaces with a single space
    date_str = re.sub(r"\s+", " ", date_str)

    # Try standard formats
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Attempt to handle custom numeric strings by stripping non-alphanumeric chars
    # E.g. '12.08.2026' -> '12/08/2026'
    cleaned_date = re.sub(r"[. ]", "/", date_str)
    try:
        dt = datetime.strptime(cleaned_date, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass

    try:
        dt = datetime.strptime(cleaned_date, "%Y/%m/%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # Safe fallback: return None (the caller preserves the original string)
    return None
