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

        # 6. Apply Inspector Crop Pass Fallback (only if not already extracted)
        if not extracted_fields.get("inspector_name"):
            inspector_fallback = get_targeted_inspector_value(image_array, reader)
            if inspector_fallback:
                extracted_fields["inspector_name"] = inspector_fallback

        # 7. Normalize Extracted Values
        normalized_fields = {}
        for field, val in extracted_fields.items():
            normalized_fields[field] = normalize_field_value(field, val)

        # Compute averages for metadata
        confidences = [d["confidence"] for d in detections]
        avg_confidence = float(np.mean(confidences)) if confidences else 0.0

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

def process_mixed_document(doc_input) -> dict:
    """
    Processes a single document input (raw file path, dictionary path, or structured bypass)
    and returns the standardized extraction result.
    """
    from ai_engine.document_processing.document_classifier import classify_document
    from ai_engine.document_processing.extractor_router import get_extractor
    
    path = None
    structured_data = None
    doc_type = None
    doc_id = None
    
    if isinstance(doc_input, str):
        path = doc_input
        doc_id = os.path.basename(path)
    elif isinstance(doc_input, dict):
        # Structured input validation (Task 10)
        doc_id = doc_input.get("document_id") or doc_input.get("path")
        if not doc_id:
            doc_id = "doc_" + str(id(doc_input))

        # Check structured bypass vs raw path
        if ("fields" in doc_input or "extracted_fields" in doc_input) and "document_type" in doc_input:
            if "extracted_fields" in doc_input:
                doc_input["fields"] = doc_input["extracted_fields"]
            structured_data = doc_input
            doc_type = doc_input["document_type"]
            # Validate field structures
            if not isinstance(doc_input.get("fields"), dict):
                raise ValueError(f"Fields object must be a dictionary in document: {doc_id}")
            # Validate document types
            valid_types = ["QCR", "TEST_DATASHEET", "QM_EFORM"]
            if doc_type not in valid_types:
                raise ValueError(f"Unsupported document type: {doc_type}")
        elif "path" in doc_input:
            path = doc_input["path"]
        else:
            raise ValueError(f"Malformed document input dictionary: {doc_input}")
    else:
        raise TypeError(f"Unsupported document input type: {type(doc_input)}")

    # 2. Determine Document Type (Classification)
    classification_confidence = 1.0
    matched_signals = []
    
    if not doc_type:
        cl_res = classify_document(path)
        doc_type = cl_res["document_type"]
        classification_confidence = cl_res["confidence"]
        matched_signals = cl_res["matched_signals"]
        
        # Unknown Document Handling (Task 11)
        if doc_type == "UNKNOWN":
            return {
                "document_id": doc_id,
                "document_type": "UNKNOWN",
                "classification_confidence": classification_confidence,
                "processing_status": "unsupported",
                "extracted_fields": {},
                "field_confidence": {},
                "metadata": {
                    "reason": "Document type could not be confidently classified.",
                    "scores": cl_res.get("scores"),
                    "matched_signals": matched_signals
                }
            }

    # 3. Retrieve Extractor from Router (Task 7)
    extractor = get_extractor(doc_type)
    if not extractor:
        return {
            "document_id": doc_id,
            "document_type": doc_type,
            "classification_confidence": classification_confidence,
            "processing_status": "unsupported",
            "extracted_fields": {},
            "field_confidence": {},
            "metadata": {
                "reason": f"No extractor registered for document type: {doc_type}"
            }
        }

    # 4. Execute Extractor and return result
    if structured_data:
        res = extractor.extract(structured_data)
    else:
        res = extractor.extract(path)
        
    res["classification_confidence"] = classification_confidence
    if "metadata" not in res:
        res["metadata"] = {}
    if matched_signals:
        res["metadata"]["classification_signals"] = matched_signals
        
    return res

def analyze_documents(document_inputs: list) -> dict:
    """
    Multi-document analysis pipeline supporting raw images and structured inputs.
    Normalizes schemas, links records, runs comparative analysis, and returns 
    structured severity/confidence discrepancy logs.
    """
    from ai_engine.data_integration.unified_data_builder import build_canonical_record
    from ai_engine.discrepancy_engine.discrepancy_detector import detect_discrepancies
    
    try:
        # 1. Validate structured input for duplicate IDs (Task 10)
        seen_ids = set()
        for doc in document_inputs:
            if isinstance(doc, dict):
                d_id = doc.get("document_id") or doc.get("path")
                if d_id:
                    if d_id in seen_ids:
                        raise ValueError(f"Duplicate document ID detected in session: {d_id}")
                    seen_ids.add(d_id)
        
        # 2. Process all documents
        processed_results = []
        warnings = []
        
        for doc in document_inputs:
            try:
                res = process_mixed_document(doc)
                processed_results.append(res)
            except Exception as e:
                warnings.append(f"Failed to process input: {str(e)}")

        # 3. Handle unknown or not_implemented documents with warnings (Task 11)
        valid_extracted = []
        for res in processed_results:
            p_status = res.get("processing_status")
            d_type = res.get("document_type")
            d_id = res.get("document_id")
            
            if p_status == "success":
                valid_extracted.append(res)
            elif p_status == "not_implemented":
                warnings.append(f"Document '{d_id}' of type '{d_type}' skipped: raw OCR extraction is not implemented.")
            elif p_status == "unsupported":
                warnings.append(f"Document '{d_id}' skipped: unsupported document format or type.")
            else:
                reason = res.get("metadata", {}).get("reason", "unknown error")
                warnings.append(f"Document '{d_id}' processing failed: {reason}")

        # 4. Check if we have valid documents left to compare
        if not valid_extracted:
            return {
                "analysis_id": "session_empty",
                "processing_status": "success",
                "documents_analyzed": 0,
                "linked_record_groups": 0,
                "summary": {
                    "total_discrepancies": 0,
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                },
                "discrepancies": [],
                "warnings": warnings
            }

        # 5. Build Canonical Records
        records = []
        for res in valid_extracted:
            fields = res.get("extracted_fields", {})
            doc_id = res.get("document_id")
            doc_type = res.get("document_type")
            ocr_meta = res.get("metadata") or {}
            
            record = build_canonical_record(doc_id, doc_type, fields, ocr_meta)
            records.append(record)

        # Deduplicate records before discrepancy detection
        from ai_engine.data_integration.deduplicator import deduplicate_records
        records = deduplicate_records(records)

        # 6. Run discrepancy engine
        discrepancies = detect_discrepancies(records)
        
        # 7. Summarize results
        total_disc = len(discrepancies)
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for disc in discrepancies:
            sev = str(disc.get("severity", "MEDIUM")).upper()
            if sev in severity_counts:
                severity_counts[sev] += 1
                
        # Programmatic verification of consistency (Task 6)
        assert sum(severity_counts.values()) == total_disc, "Summary counts mismatch in pipeline."
                
        # Group IDs
        group_ids = set(disc.get("group_id", "GROUP-1") for disc in discrepancies)
        
        return {
            "analysis_id": "session_" + str(len(records)),
            "processing_status": "success",
            "documents_analyzed": len(records),
            "linked_record_groups": len(group_ids) if group_ids else 1,
            "summary": {
                "total_discrepancies": total_disc,
                "critical": severity_counts["CRITICAL"],
                "high": severity_counts["HIGH"],
                "medium": severity_counts["MEDIUM"],
                "low": severity_counts["LOW"]
            },
            "discrepancies": discrepancies,
            "warnings": warnings
        }
    except Exception as e:
        print(f"[Pipeline Error] analyze_documents failed: {str(e)}")
        # Fail gracefully, but do not return raw tracebacks (Task 12)
        return {
            "analysis_id": "failed_session",
            "processing_status": "failed",
            "documents_analyzed": 0,
            "linked_record_groups": 0,
            "summary": {
                "total_discrepancies": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "discrepancies": [],
            "error": f"Document analysis failed: {str(e)}"
        }


