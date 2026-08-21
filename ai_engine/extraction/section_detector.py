def detect_sections(lines: list) -> dict:
    """
    Scans reconstructed lines for section headers and returns a mapping
    of section names to vertical coordinate ranges (y_start, y_end).
    """
    y_coords = {}
    
    # Standard section keywords
    section_mapping = {
        "project": ["project details", "general information", "project identification"],
        "inspection": ["inspection details", "inspector information", "monitoring details"],
        "quality": ["quality observations", "measurements", "observation fields", "measurement table"],
        "remarks": ["remarks", "remarks section", "notes"]
    }

    for line in lines:
        text_lower = line["text"].lower()
        for sect, keywords in section_mapping.items():
            if any(kw in text_lower for kw in keywords):
                # Save the y coordinate of the header line
                y_coords[sect] = line["y"]
                break

    # Sort sections vertically
    sorted_sects = sorted([k for k, v in y_coords.items() if v is not None], key=lambda k: y_coords[k])
    
    sections = {}
    for i, sect_name in enumerate(sorted_sects):
        start_y = y_coords[sect_name]
        end_y = y_coords[sorted_sects[i+1]] if i + 1 < len(sorted_sects) else float("inf")
        sections[sect_name] = (start_y, end_y)
        
    return sections

def get_section_for_yc(yc: float, sections: dict) -> str:
    """
    Returns the section name for a given vertical coordinate yc, or 'unknown'.
    """
    for sect_name, (start, end) in sections.items():
        if start <= yc < end:
            return sect_name
    return "unknown"
