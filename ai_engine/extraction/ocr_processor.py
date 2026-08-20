import re
import numpy as np

_reader = None

def get_reader():
    """
    Lazy load and initialize EasyOCR English Reader.
    """
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

def get_box_geometry(box):
    """
    Extract geometric centers and dimensions for layout parsing from OCR boxes.
    """
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
    """
    Applies geometry logic and packages the raw OCR word arrays.
    """
    from ai_engine.preprocessing.text_cleaner import normalize_ocr_text
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

def targeted_inspector_ocr(image_array, reader):
    """
    Pre-processes and crops an image to perform high-resolution text matching for inspector details.
    """
    import cv2
    
    # Handle cases where image is not yet a numpy array (cv2 format)
    image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    h, w = image_bgr.shape[:2]
    
    # Specific layout crop dimensions for typical PMGSY QCR forms
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

def get_targeted_inspector_value(image_array, reader):
    """
    Runs the targeted cropped OCR pass and joins the resultant text lines.
    """
    try:
        results = targeted_inspector_ocr(image_array, reader)
        texts = [
            str(text).strip()
            for _, text, confidence in results
            if float(confidence) >= 0.5
        ]
        return " ".join(texts).strip() if texts else None
    except Exception as e:
        print(f"[OCR Processor Exception] Targeted inspector OCR failed: {str(e)}")
        return None
