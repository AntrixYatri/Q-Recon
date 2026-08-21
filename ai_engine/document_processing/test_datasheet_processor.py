import os
import io
import numpy as np
from PIL import Image
from ai_engine.document_processing.base_extractor import BaseDocumentExtractor
from ai_engine.extraction.easyocr_engine import get_reader
from ai_engine.extraction.detection_processor import prepare_detections
from ai_engine.extraction.line_reconstruction import group_into_lines
from ai_engine.extraction.key_value_extractor import extract_key_values_from_lines
from ai_engine.extraction.table_extractor import extract_table_from_detections
from ai_engine.preprocessing.field_normalizer import normalize_field_value
from ai_engine.preprocessing.schema_normalizer import normalize_field_name

class TestDatasheetProcessor(BaseDocumentExtractor):
    """
    Test Datasheet Extractor utilizing real EasyOCR layout-aware, table-aware,
    and key-value parsing pipelines. Supports PDF processing with PyMuPDF.
    """
    def extract(self, document_path_or_dict) -> dict:
        # 1. Structured input bypass (Task 5)
        if isinstance(document_path_or_dict, dict):
            fields = document_path_or_dict.get("fields", {})
            return {
                "document_id": document_path_or_dict.get("document_id", "test_datasheet_doc"),
                "document_type": "TEST_DATASHEET",
                "classification_confidence": 1.0,
                "processing_status": "success",
                "extracted_fields": fields,
                "field_confidence": {k: 1.0 for k in fields.keys()},
                "metadata": {"source": "structured_input_bypass"}
            }

        document_path = document_path_or_dict
        doc_id = os.path.basename(document_path)
        
        # 2. PDF Processing & Dependency Check
        image_array = None
        
        if document_path.lower().endswith(".pdf"):
            try:
                import fitz # PyMuPDF
            except ImportError:
                return {
                    "document_id": doc_id,
                    "document_type": "TEST_DATASHEET",
                    "classification_confidence": 0.0,
                    "processing_status": "unsupported",
                    "error_type": "pdf_processing_unavailable",
                    "message": "PDF processing requires PyMuPDF, which is unavailable in the current environment.",
                    "extracted_fields": {},
                    "field_confidence": {},
                    "metadata": {}
                }
            
            try:
                doc = fitz.open(document_path)
                if doc.page_count < 1:
                    raise ValueError("PDF contains no pages")
                page = doc.load_page(0)
                # Render at 150 DPI for robust OCR on CPU
                pix = page.get_pixmap(dpi=150)
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data)).convert("RGB")
                image_array = np.ascontiguousarray(np.asarray(image))
            except Exception as e:
                return {
                    "document_id": doc_id,
                    "document_type": "TEST_DATASHEET",
                    "classification_confidence": 0.0,
                    "processing_status": "failed",
                    "error_type": "invalid_or_unreadable_pdf",
                    "message": f"Failed to render PDF: {str(e)}",
                    "extracted_fields": {},
                    "field_confidence": {},
                    "metadata": {}
                }
        else:
            # Standard PNG/JPG image processing
            try:
                if not os.path.exists(document_path):
                    raise FileNotFoundError(f"Image path does not exist: {document_path}")
                image = Image.open(document_path).convert("RGB")
                image_array = np.ascontiguousarray(np.asarray(image))
            except Exception as e:
                return {
                    "document_id": doc_id,
                    "document_type": "TEST_DATASHEET",
                    "classification_confidence": 0.0,
                    "processing_status": "failed",
                    "error_type": "file_error",
                    "message": str(e),
                    "extracted_fields": {},
                    "field_confidence": {},
                    "metadata": {}
                }

        # 3. Run OCR extraction
        try:
            reader = get_reader()
            ocr_result = reader.readtext(image_array, detail=1, paragraph=False)
            detections = prepare_detections(ocr_result)
            # Reconstruct lines with dynamic column segmenting for metadata above the table header Y position
            all_lines = group_into_lines(detections)
            header_y = None
            header_keywords = ["parameter", "required", "measured", "unit", "result", "value", "status"]
            for line in all_lines:
                line_text = line["text"].lower()
                matched_count = sum(1 for kw in header_keywords if kw in line_text)
                if matched_count >= 2:
                    header_y = line["y"]
                    break

            split_y = header_y if header_y is not None else 650
            
            meta_detections = [d for d in detections if d["yc"] < split_y]
            lower_detections = [d for d in detections if d["yc"] >= split_y]

            left_meta = [d for d in meta_detections if d["xc"] < 800]
            right_meta = [d for d in meta_detections if d["xc"] >= 800]

            left_lines = group_into_lines(left_meta)
            right_lines = group_into_lines(right_meta)
            lower_lines = group_into_lines(lower_detections)

            lines = left_lines + right_lines + lower_lines

            # 4. Run Table and Key-Value extraction
            kv_fields = extract_key_values_from_lines(lines)
            table_rows = extract_table_from_detections(detections)

            extracted_fields = {}
            
            # Map key-value fields first
            for k, v in kv_fields.items():
                extracted_fields[k] = v

            # Map table fields
            candidate_rows = []
            for row in table_rows:
                canon_row = {}
                for r_key, r_val in row.items():
                    canon_key = normalize_field_name(r_key)
                    if canon_key:
                        canon_row[canon_key] = r_val
                if canon_row:
                    candidate_rows.append(canon_row)

            # Find the best row matching parameter or fallback
            best_row = {}
            if candidate_rows:
                known_parameters = ["pavement thickness", "compaction", "aggregate size"]
                for crow in candidate_rows:
                    param_val = str(crow.get("parameter", "")).lower()
                    if any(p in param_val for p in known_parameters):
                        best_row = crow
                        break
                if not best_row:
                    best_row = candidate_rows[0]

            # Merge best table row into extracted fields
            for r_key, r_val in best_row.items():
                if r_val:
                    if r_key in ["parameter", "measured_value", "required_value", "unit", "quality_status"]:
                        extracted_fields[r_key] = r_val

            # Ambiguity handling for measured_value (Step 12)
            ambiguities = {}
            measured_candidates = []
            for crow in candidate_rows:
                m_val = crow.get("measured_value")
                if m_val and m_val not in measured_candidates:
                    measured_candidates.append(m_val)
            
            if "measured_value" in kv_fields and kv_fields["measured_value"] not in measured_candidates:
                measured_candidates.append(kv_fields["measured_value"])

            if len(measured_candidates) > 1:
                ambiguities["measured_value"] = {
                    "status": "ambiguous",
                    "candidates": measured_candidates
                }

            # 5. Normalize Extracted Values
            normalized_fields = {}
            for field, val in extracted_fields.items():
                normalized_fields[field] = normalize_field_value(field, val)

            # Compute baseline confidence
            confidences = [d["confidence"] for d in detections]
            avg_confidence = float(np.mean(confidences)) if confidences else 0.0

            field_confidence = {}
            for field in normalized_fields.keys():
                field_confidence[field] = round(avg_confidence, 2)

            return {
                "document_id": doc_id,
                "document_type": "TEST_DATASHEET",
                "classification_confidence": 1.0,
                "processing_status": "success",
                "extracted_fields": normalized_fields,
                "field_confidence": field_confidence,
                "metadata": {
                    "ocr_confidence": round(avg_confidence, 2),
                    "detections_count": len(detections),
                    "ocr_engine": "EasyOCR",
                    "ambiguities": ambiguities
                }
            }

        except Exception as e:
            return {
                "document_id": doc_id,
                "document_type": "TEST_DATASHEET",
                "classification_confidence": 0.0,
                "processing_status": "failed",
                "error_type": "extraction_error",
                "message": str(e),
                "extracted_fields": {},
                "field_confidence": {},
                "metadata": {}
            }
