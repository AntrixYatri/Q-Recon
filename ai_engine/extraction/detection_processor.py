from ai_engine.extraction.layout_utils import get_box_geometry
from ai_engine.preprocessing.ocr_normalizer import normalize_ocr_text

def prepare_detections(ocr_result: list) -> list:
    """
    Transforms raw EasyOCR detections list into layout dictionaries.
    Each object contains: normalized text, confidence, original box, and geometric dimensions.
    """
    detections = []
    for detection in ocr_result:
        box, text, confidence = detection
        geom = get_box_geometry(box)

        detections.append({
            "text": normalize_ocr_text(text),
            "confidence": float(confidence),
            "box": box,
            **geom
        })
    return detections
