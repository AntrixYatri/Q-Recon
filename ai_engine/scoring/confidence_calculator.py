def calculate_confidence(discrepancy: dict) -> dict:
    """
    Computes a confidence score (0.0 to 1.0) and level (LOW, MEDIUM, HIGH)
    for a discrepancy based on OCR scanning quality, document linking, and parsing success.
    """
    ocr_confidence = 1.0
    record_link_confidence = 1.0
    normalization_success = True

    involved_docs = discrepancy.get("documents", [])
    
    # 1. Evaluate OCR quality factor
    ocr_confs = []
    for doc in involved_docs:
        conf = doc.get("ocr_confidence")
        if conf is not None:
            # Map percentages to decimals (Task 2)
            if conf > 1.0:
                conf = float(conf) / 100.0
            ocr_confs.append(float(conf))
            
    if ocr_confs:
        ocr_confidence = sum(ocr_confs) / len(ocr_confs)

    # 2. Evaluate linking factor
    # For ambiguous conflicts with ties, reduce linking/discrepancy confidence (Task 3)
    if discrepancy.get("comparison_status") == "ambiguous" or discrepancy.get("discrepancy_type") == "ambiguous_conflict":
        record_link_confidence = 0.75
    else:
        record_link_confidence = 0.95

    # 3. Evaluate normalization factor
    # If there is a parsing error, normalization_success is marked False
    if "error" in discrepancy:
        normalization_success = False

    # Calculate aggregate confidence score (0.0 to 1.0)
    norm_factor = 1.0 if normalization_success else 0.5
    score = round(ocr_confidence * record_link_confidence * norm_factor, 2)

    # Assign level string
    if score >= 0.85:
        level = "HIGH"
    elif score >= 0.70:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "confidence_score": score,
        "confidence_level": level,
        "factors": {
            "ocr_confidence": round(ocr_confidence, 2),
            "record_link_confidence": round(record_link_confidence, 2),
            "normalization_success": normalization_success
        }
    }

# Post-processing normalization helper functions.
