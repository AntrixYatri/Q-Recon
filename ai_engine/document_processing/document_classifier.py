import os
from ai_engine.document_processing.classification_config import CLASSIFICATION_CONFIG

def classify_document(document_path: str, ocr_text: str = None) -> dict:
    """
    Classifies a document as QCR, TEST_DATASHEET, QM_EFORM, or UNKNOWN
    using explainable, weighted-keyword signals and filename hints.
    """
    doc_types = CLASSIFICATION_CONFIG["document_types"]
    signals = CLASSIFICATION_CONFIG["weighted_signals"]
    hints = CLASSIFICATION_CONFIG["filename_hints"]
    threshold = CLASSIFICATION_CONFIG["confidence_threshold"]
    
    # 1. Obtain search text
    text_content = ""
    if ocr_text:
        text_content = ocr_text
    elif os.path.exists(document_path):
        # Fallback: Read text file or run simple EasyOCR scan if it's an image
        filename_lower = os.path.basename(document_path).lower()
        is_image = any(filename_lower.endswith(ext) for ext in [".png", ".jpg", ".jpeg"])
        
        if is_image:
            try:
                from ai_engine.extraction.easyocr_engine import get_reader
                reader = get_reader()
                results = reader.readtext(document_path)
                text_content = " ".join(res[1] for res in results)
            except Exception as e:
                print(f"[Classifier Warning] EasyOCR scan failed: {str(e)}")
        else:
            try:
                with open(document_path, "r", encoding="utf-8", errors="ignore") as f:
                    text_content = f.read()
            except Exception:
                pass

    text_lower = text_content.lower()
    filename_lower = os.path.basename(document_path).lower()

    # 2. Compute scores and matched signals
    scores = {t: 0.0 for t in signals.keys()}
    matched_signals = []

    for doc_type, kw_weights in signals.items():
        # Match keywords
        for kw, weight in kw_weights.items():
            if kw in text_lower:
                scores[doc_type] += weight
                matched_signals.append(kw)

        # Match filename hints as a weak fallback (adds up to 0.15)
        for hint in hints.get(doc_type, []):
            if hint in filename_lower:
                scores[doc_type] += 0.15
                matched_signals.append(f"filename_hint:{hint}")

    # Normalize/cap scores between 0.0 and 1.0
    for doc_type in scores:
        scores[doc_type] = round(min(scores[doc_type], 1.0), 2)

    # 3. Determine best classification
    best_type = "UNKNOWN"
    best_score = 0.0

    if scores:
        sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_type, top_score = sorted_types[0]
        
        if top_score >= threshold:
            best_type = top_type
            best_score = top_score
        else:
            best_type = "UNKNOWN"
            best_score = top_score

    return {
        "document_type": best_type,
        "confidence": best_score,
        "scores": scores,
        "matched_signals": list(set(matched_signals))
    }
