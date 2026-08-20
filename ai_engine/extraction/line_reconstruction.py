import numpy as np
from ai_engine.preprocessing.ocr_normalizer import normalize_ocr_text

def group_into_lines(detections: list) -> list:
    """
    Reconstructs visual text lines from bounding boxes.
    Sorts detections top-to-bottom, groups adjacent boxes vertically,
    sorts horizontal lines left-to-right, and joins strings.
    """
    if not detections:
        return []

    # Sort top-to-bottom
    detections = sorted(detections, key=lambda d: d["yc"])

    lines = []
    for det in detections:
        placed = False
        for line in lines:
            avg_y = np.mean([item["yc"] for item in line])
            avg_h = np.mean([item["height"] for item in line])

            # Check horizontal alignment threshold (65% of character height or 12px)
            if abs(det["yc"] - avg_y) <= max(avg_h * 0.65, 12):
                line.append(det)
                placed = True
                break

        if not placed:
            lines.append([det])

    # Sort each line left-to-right
    for line in lines:
        line.sort(key=lambda d: d["x1"])

    # Convert to structured lines
    reconstructed_lines = []
    for line in lines:
        text = " ".join(item["text"] for item in line)
        reconstructed_lines.append({
            "text": normalize_ocr_text(text),
            "detections": line,
            "y": np.mean([item["yc"] for item in line])
        })

    # Sort final reconstructed lines top-to-bottom
    reconstructed_lines.sort(key=lambda x: x["y"])
    return reconstructed_lines
