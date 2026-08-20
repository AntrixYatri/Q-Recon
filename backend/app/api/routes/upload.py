from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.document_service import DocumentService
from app.services.extraction_service import ExtractionService
from app.models.response_models import UploadResponse
import os

router = APIRouter()

@router.post("", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form("qcr")
):
    """
    Ingest a quality control record image or PDF, parse via OCR, and return extracted metrics.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file: Missing name")

    try:
        # Save to disk
        saved_path = await DocumentService.save_upload(file)
        
        # Read bytes for OCR processor
        file_bytes = DocumentService.read_file_bytes(saved_path)
        
        # Determine mime type from extension if missing
        mime_type = file.content_type or ("application/pdf" if file.filename.endswith(".pdf") else "image/png")
        
        # Run AI extractor
        extraction_result = ExtractionService.extract_document(
            file_bytes=file_bytes,
            filename=file.filename,
            mime_type=mime_type
        )
        
        # Assign a mock analysis ID linked to this upload
        analysis_id = "proj-101"
        
        return UploadResponse(
            success=True,
            analysis_id=analysis_id,
            filename=file.filename,
            ocr_confidence=extraction_result.get("ocr_confidence", 0.0),
            extracted_fields=extraction_result.get("extracted_fields", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
