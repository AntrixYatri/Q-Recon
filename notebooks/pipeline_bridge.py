"""
QCR PIPELINE BRIDGE
Built from the OCR workflow in the SIH_QCR_AI_Engine notebook.

This bridge accepts Streamlit-uploaded bytes, converts them to a supported
EasyOCR input (NumPy array), runs the OCR workflow, reconstructs lines,
extracts QCR fields, and performs the targeted Inspector OCR pass.

Handwritten OCR is NOT claimed here.
"""

import io
import re
import numpy as np
from PIL import Image


# ------------------------------------------------------------
# Lazy OCR model
# ------------------------------------------------------------
_reader = None


def get_reader():
    global _reader

    if _reader is None:
        import easyocr

        try:
            import torch
            use_gpu = bool(torch.cuda.is_available())
        except Exception:
            use_gpu = False

        _reader = easyocr.Reader(["en"], gpu=use_gpu)

    return _reader


# ------------------------------------------------------------
# OCR utilities
# ------------------------------------------------------------
def normalize_ocr_text(text):
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" :", ":")
    text = re.sub(r":\s*", ": ", text)
    return text.strip()


def get_box_geometry(box):
    xs = [point[0] for point in box]
    ys = [point[1] for point in box]

    return {
        "x1": min(xs),
        "y1": min(ys),
        "x2": max(xs),
        "y2": max(ys),
        "xc": sum(xs) / len(xs),
        "yc": sum(ys) / len(ys),
        "width": max(xs) - min(xs),
        "height": max(ys) - min(ys),
    }


def prepare_detections(ocr_result):
    detections = []

    for detection in ocr_result:
        box, text, confidence = detection
        geom = get_box_geometry(box)

        detections.append({
            "text": normalize_ocr_text(text),
            "confidence": float(confidence),
            "box": box,
            **geom,
        })

    return detections


def group_into_lines(detections):
    if not detections:
        return []

    detections = sorted(detections, key=lambda d: d["yc"])
    lines = []

    for det in detections:
        placed = False

        for line in lines:
            avg_y = np.mean([item["yc"] for item in line])
            avg_h = np.mean([item["height"] for item in line])

            if abs(det["yc"] - avg_y) <= max(avg_h * 0.65, 12):
                line.append(det)
                placed = True
                break

        if not placed:
            lines.append([det])

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


# ------------------------------------------------------------
# QCR field extraction
# ------------------------------------------------------------
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


def clean_label(label):
    label = normalize_ocr_text(label)
    label = label.lower()
    label = label.replace(":", "")
    return label.strip()


def extract_from_reconstructed_lines(lines):
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

                    if i + 1 < len(normalized_lines):
                        next_value = normalized_lines[i + 1]["original"]
                        extracted[field] = next_value.strip()
                        break

            if field in extracted:
                break

    return extracted


# ------------------------------------------------------------
# Targeted Inspector OCR
# ------------------------------------------------------------
def targeted_inspector_ocr(image, reader):
    import cv2

    image_rgb = np.array(image.convert("RGB"))
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    h, w = image_bgr.shape[:2]

    x1 = min(350, w)
    x2 = min(w, 700)
    y1 = min(925, h)
    y2 = min(1005, h)

    if x2 <= x1 or y2 <= y1:
        return []

    crop = image_bgr[y1:y2, x1:x2]

    enlarged = cv2.resize(
        crop,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC,
    )

    gray = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    return reader.readtext(
        np.ascontiguousarray(gray),
        detail=1,
        paragraph=False,
    )


def get_targeted_inspector_value(image, reader):
    try:
        results = targeted_inspector_ocr(image, reader)

        texts = [
            str(text).strip()
            for _, text, confidence in results
            if float(confidence) >= 0.5
        ]

        return " ".join(texts).strip() if texts else None

    except Exception:
        return None


# ------------------------------------------------------------
# Main Streamlit entry point
# ------------------------------------------------------------
def process_evidence(file_bytes, filename, mime_type):
    """
    Run the real OCR + structured extraction pipeline.

    IMPORTANT FIX:
    Streamlit gives us raw uploaded bytes. EasyOCR does not accept a PIL
    Image object directly, so the image is converted to a NumPy RGB array
    before reader.readtext().
    """

    if mime_type == "application/pdf" or filename.lower().endswith(".pdf"):
        raise ValueError(
            "PDF input is not wired into the current notebook OCR pipeline. "
            "Use a PNG/JPG/WEBP image for this prototype."
        )

    # 1. Bytes -> PIL
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")

    # 2. PIL -> NumPy
    # This is the fix for:
    # ValueError: Invalid input type. Supporting format =
    # string(file path or url), bytes, numpy array
    image_array = np.ascontiguousarray(np.asarray(image))

    # 3. Load the same EasyOCR model used by the notebook
    reader = get_reader()

    # 4. Main OCR
    ocr_result = reader.readtext(
        image_array,
        detail=1,
        paragraph=False,
    )

    # 5. Notebook-style processing
    detections = prepare_detections(ocr_result)
    lines = group_into_lines(detections)
    extracted = extract_from_reconstructed_lines(lines)

    # 6. Targeted Inspector fallback
    inspector_fallback = get_targeted_inspector_value(image, reader)
    if inspector_fallback:
        extracted["inspector_name"] = inspector_fallback

    # 7. Average OCR confidence
    confidences = [d["confidence"] for d in detections]
    avg_confidence = (
        float(np.mean(confidences)) * 100
        if confidences else None
    )

    quality_status = extracted.get("quality_status")
    status = quality_status.upper() if quality_status else "OCR COMPLETE"

    return {
        "status": status,
        "ocr_confidence": avg_confidence,
        "ocr_text": "\n".join(line["text"] for line in lines),
        "extracted_fields": extracted,
        "detections": len(detections),
        "handwritten_ocr": "Not validated",
        "details": {
            "engine": "EasyOCR",
            "language": "English",
            "line_reconstruction": True,
            "targeted_inspector_pass": bool(inspector_fallback),
            "note": (
                "Current notebook validation is based on synthetic "
                "PMGSY-grounded QCR images."
            ),
        },
    }
