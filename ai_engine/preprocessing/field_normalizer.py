import re

def normalize_field_value(field: str, value) -> str:
    """
    Standardises and cleans extracted values based on the field type.
    """
    if value is None:
        return ""

    value = str(value).strip().lower()

    # General whitespace normalization
    value = re.sub(r"\s+", " ", value)

    # 1. Report Number Field Specifics
    if field == "report_number":
        # Remove spaces around hyphens
        value = re.sub(r"\s*-\s*", "-", value)
        # Collapse all inner spaces
        value = value.replace(" ", "")

    # 2. Text Fields Specifics
    elif field in [
        "state",
        "district",
        "block",
        "habitation_name",
        "facility_name",
        "facility_category",
        "facility_subcategory",
        "inspection_type",
        "inspector_name",
        "quality_status"
    ]:
        value = re.sub(r"\s+", " ", value)

    return value.strip()
