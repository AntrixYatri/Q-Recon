import re

def extract_qcr_fields(ocr_text: str) -> dict:
    """
    Regex-based text field extraction strategy from raw unaligned OCR text string.
    Useful as a fallback or parallel pipeline to layout-aware extraction.
    """
    extracted = {}

    def find_value(pattern):
        match = re.search(pattern, ocr_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    # Header fields
    extracted["report_number"] = find_value(r"Report Number:\s*(.+)")
    extracted["project_name"] = find_value(r"Project Name:\s*(.+)")
    extracted["project_code"] = find_value(r"Project Code:\s*(.+)")

    # Location
    extracted["state"] = find_value(r"State:\s*(.+)")
    extracted["district"] = find_value(r"District:\s*(.+)")
    extracted["block"] = find_value(r"Block:\s*(.+)")
    extracted["village"] = find_value(r"Village:\s*(.+)")

    # Road
    extracted["road_name"] = find_value(r"Road Name:\s*(.+)")
    extracted["road_code"] = find_value(r"Road Code:\s*(.+)")
    extracted["road_length"] = find_value(r"Road Length:\s*(.+)")
    extracted["road_category"] = find_value(r"Road Category:\s*(.+)")

    # Inspection
    extracted["inspection_date"] = find_value(r"Inspection Date:\s*(.+)")
    extracted["inspection_type"] = find_value(r"Inspection Type:\s*(.+)")
    extracted["inspector_name"] = find_value(r"Inspector:\s*(.+)")
    extracted["inspection_location"] = find_value(r"Location:\s*(.+)")

    # Quality information
    extracted["parameter"] = find_value(r"Parameter\s*\n?([A-Za-z ]+)")
    extracted["required_value"] = find_value(r"Required Value\s*\n?([0-9.]+)")
    extracted["measured_value"] = find_value(r"Measured Value\s*\n?([0-9.]+)")
    extracted["unit"] = find_value(r"Unit\s*\n?([A-Za-z%]+)")
    extracted["quality_status"] = find_value(r"Quality Status:\s*(.+)")

    # Other fields
    extracted["contractor_name"] = find_value(r"Contractor:\s*(.+)")
    extracted["agency_name"] = find_value(r"Agency:\s*(.+)")

    return extracted
