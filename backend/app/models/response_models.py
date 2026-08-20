from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class HealthResponse(BaseModel):
    status: str = Field(default="ok")
    service: str = Field(default="QCR AI Backend Service")

class DiscrepancyItem(BaseModel):
    id: str
    field: str
    document_a: str
    document_b: str
    value_a: str
    value_b: str
    discrepancy_type: str
    severity: str
    confidence: float
    explanation: str

class AnalysisSummary(BaseModel):
    documents_analyzed: int
    total_discrepancies: int
    critical: int
    warning: int
    minor: int

class ProjectDetails(BaseModel):
    road_name: str
    package_id: str
    district: str
    state: str

class AnalysisResultResponse(BaseModel):
    analysis_id: str
    project: ProjectDetails
    summary: AnalysisSummary
    discrepancies: List[DiscrepancyItem]

class UploadResponse(BaseModel):
    success: bool
    analysis_id: str
    filename: str
    ocr_confidence: float
    extracted_fields: Dict[str, Any]
