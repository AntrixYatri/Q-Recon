import os
import numpy as np
from ai_engine.config.settings import TARGETED_INSPECTOR_CROP

def targeted_inspector_ocr(image_input, reader) -> tuple:
    """
    Performs focused, second-pass OCR on the Inspector field region.
    Supports either an image filepath string or a pre-loaded BGR NumPy array.
    """
    try:
        import cv2
    except ImportError:
        print("[Targeted OCR Warning] cv2 (OpenCV) is not installed. Cropped OCR fallback is disabled.")
        return None

    if isinstance(image_input, str):
        if not os.path.exists(image_input):
            return None
        image = cv2.imread(image_input)
    elif isinstance(image_input, np.ndarray):
        # Already a NumPy array, copy it to avoid mutations
        image = image_input.copy()
    else:
        # Fallback for PIL Image or other formats
        image = np.array(image_input)

    if image is None or len(image.shape) < 2:
        return None

    h, w = image.shape[:2]

    # Configurable layout crop coordinates for the generated QCR templates
    x1 = TARGETED_INSPECTOR_CROP["x1"]
    x2 = min(w, TARGETED_INSPECTOR_CROP["x2_max_offset"])
    y1 = TARGETED_INSPECTOR_CROP["y1"]
    y2 = min(h, TARGETED_INSPECTOR_CROP["y2_max_offset"])

    if x2 <= x1 or y2 <= y1:
        return None

    # Slice Inspector bounding region
    crop = image[y1:y2, x1:x2]

    # Pre-processing enhancements: upscale, grayscale, and histogram equalization
    scale = 4
    enlarged = cv2.resize(
        crop,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )
    
    # Check if image has color channels before converting
    if len(enlarged.shape) == 3:
        gray = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY)
    else:
        gray = enlarged
        
    gray_enhanced = cv2.equalizeHist(gray)

    # Perform EasyOCR read
    results = reader.readtext(
        gray_enhanced,
        detail=1,
        paragraph=False
    )

    return results, crop, enlarged

def get_targeted_inspector_value(image_input, reader) -> str:
    """
    Extracts and concatenates high-confidence characters from the inspector crop.
    """
    try:
        ocr_out = targeted_inspector_ocr(image_input, reader)
        if ocr_out is None:
            return None
            
        results, _, _ = ocr_out
        texts = [
            str(text).strip()
            for _, text, confidence in results
            if float(confidence) >= 0.5
        ]

        if not texts:
            return None

        return " ".join(texts).strip()
    except Exception as e:
        print(f"[Targeted OCR Warning] Inspector fallback failed: {str(e)}")
        return None
