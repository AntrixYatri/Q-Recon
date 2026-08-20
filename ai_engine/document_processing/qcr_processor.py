import numpy as np
from ai_engine.preprocessing.text_cleaner import clean_label, normalize_ocr_text

FIELD_LABELS = {
    "report_number": ["Report Number"],
    "state": ["State"],
    "district": ["District"],
    "block": ["Block"],
    "habitation_name": ["Habitation"],
    "habitation_id": ["Habitation ID"],
    "facility_name": ["Facility"],
    "facility_category": ["Category"],
    "facility_subcategory": ["Subcategory"],
    "inspection_date": ["Inspection Date"],
    "inspection_type": ["Inspection Type"],
    "inspector_name": ["Inspector"],
    "quality_status": ["QUALITY STATUS"],
}

def group_into_lines(detections):
    """
    Groups bounding boxes into horizontal lines based on y-coordinate overlaps.
    """
    if not detections:
        return []

    # Sort detections by Y center coordinate
    detections = sorted(detections, key=lambda d: d["yc"])
    lines = []

    for det in detections:
        placed = False
        for line in lines:
            avg_y = np.mean([item["yc"] for item in line])
            avg_h = np.mean([item["height"] for item in line])

            # Group words in same line if Y gap is within threshold
            if abs(det["yc"] - avg_y) <= max(avg_h * 0.65, 12):
                line.append(det)
                placed = True
                break

        if not placed:
            lines.append([det])

    # Sort each line from left to right (X coordinate)
    for line in lines:
        line.sort(key=lambda d: d["x1"])

    reconstructed_lines = []
    for line in lines:
        text = " ".join(item["text"] for item in line)
        reconstructed_lines.append({
            "text": normalize_ocr_text(text),
            "detections": line,
            "y": np.mean([item["yc"] for item in line]),
        })

    reconstructed_lines.sort(key=lambda x: x["y"])
    return reconstructed_lines

def extract_from_reconstructed_lines(lines):
    """
    Searches the reconstructed text lines for key form labels and extracts their values.
    """
    extracted = {}
    normalized_lines = [
        {
            "text": clean_label(line["text"]),
            "original": line["text"],
        }
        for line in lines
    ]

    for field, labels in FIELD_LABELS.items():
        for i, line in enumerate(normalized_lines):
            line_text = line["text"]
            for label in labels:
                label_clean = clean_label(label)

                if line_text.startswith(label_clean):
                    value = line_text[len(label_clean):].strip()
                    value = value.lstrip(":")

                    if value:
                        extracted[field] = value.strip()
                        break

                    # Fallback to the next line if the label value is empty
                    if i + 1 < len(normalized_lines):
                        next_value = normalized_lines[i + 1]["original"]
                        extracted[field] = next_value.strip()
                        break

            if field in extracted:
                break

    return extracted
