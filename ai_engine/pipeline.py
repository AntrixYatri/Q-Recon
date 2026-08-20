import os
import io
import numpy as np
from PIL import Image
from ai_engine.extraction.easyocr_engine import get_reader
from ai_engine.extraction.detection_processor import prepare_detections
from ai_engine.extraction.line_reconstruction import group_into_lines
from ai_engine.extraction.targeted_ocr import get_targeted_inspector_value
from ai_engine.document_processing.layout_field_extractor import extract_from_reconstructed_lines
from ai_engine.preprocessing.field_normalizer import normalize_field_value

def analyze_document(image_input) -> dict:
    """
    Main entry point for document OCR, layout reconstruction, field extraction, 
    and value normalization.
    
    Accepts either an image filepath string or raw image bytes.
    """
    try:
        # 1. Load Image BGR array
        if isinstance(image_input, (str, os.PathLike)):
            if not os.path.exists(image_input):
                raise FileNotFoundError(f"Image path does not exist: {image_input}")
            # Open with PIL and convert to RGB array
            image = Image.open(image_input).convert("RGB")
            image_array = np.ascontiguousarray(np.asarray(image))
            doc_id = os.path.basename(image_input)
        elif isinstance(image_input, bytes):
            image = Image.open(io.BytesIO(image_input)).convert("RGB")
            image_array = np.ascontiguousarray(np.asarray(image))
            doc_id = "uploaded_document"
        else:
            # Assume it is already a numpy array/PIL image
            image = Image.fromarray(image_input) if isinstance(image_input, np.ndarray) else image_input
            image_array = np.ascontiguousarray(np.asarray(image))
            doc_id = "in_memory_image"

        # 2. Run EasyOCR English Reader
        reader = get_reader()
        ocr_result = reader.readtext(image_array, detail=1, paragraph=False)

        # 3. Visual Bounding Box Geometry Prep
        detections = prepare_detections(ocr_result)

        # 4. Horizontal Line Reconstruction
        lines = group_into_lines(detections)

        # 5. Schema Mapped Field Extraction
        extracted_fields = extract_from_reconstructed_lines(lines)

        # 6. Apply Inspector Crop Pass Fallback
        inspector_fallback = get_targeted_inspector_value(image_array, reader)
        if inspector_fallback:
            extracted_fields["inspector_name"] = inspector_fallback

        # 7. Normalize Extracted Values
        normalized_fields = {}
        for field, val in extracted_fields.items():
            normalized_fields[field] = normalize_field_value(field, val)

        # Compute averages for metadata
        confidences = [d["confidence"] for d in detections]
        avg_confidence = float(np.mean(confidences)) * 100 if confidences else 0.0

        # Construct field confidence mappings
        field_confidence = {}
        for field in normalized_fields.keys():
            # In a production system, we map the bounding box confidence of the specific field detection.
            # Here we assign the average OCR confidence of the page as a baseline indicator.
            field_confidence[field] = round(avg_confidence, 2)

        return {
            "document_id": doc_id,
            "document_type": "QCR",
            "extracted_fields": normalized_fields,
            "field_confidence": field_confidence,
            "ocr_metadata": {
                "ocr_confidence": round(avg_confidence, 2),
                "detections_count": len(detections),
                "ocr_engine": "EasyOCR"
            },
            "processing_status": "success"
        }

    except Exception as e:
        print(f"[Pipeline Exception] analyze_document failed: {str(e)}")
        return {
            "document_id": "unknown",
            "document_type": "QCR",
            "extracted_fields": {},
            "field_confidence": {},
            "ocr_metadata": {
                "ocr_confidence": 0.0,
                "error": str(e)
            },
            "processing_status": "failed"
        }

def run_discrepancy_pipeline(analysis_id: str) -> dict:
    """
    Combines extracted documents, performs schema mapping, links records, 
    compares values, and returns a comprehensive discrepancy audit log.
    """
    from ai_engine.discrepancy_engine.discrepancy_detector import compare_documents
    return compare_documents(analysis_id)

