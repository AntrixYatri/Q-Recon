from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class HealthResponse(BaseModel):
    status: str = Field(default="ok")
    service: str = Field(default="QCR AI Backend Service")

class DiscrepancyDocument(BaseModel):
    document_id: str
    document_type: str
    value: Optional[str] = None
    normalized_value: Optional[str] = None
    ocr_confidence: Optional[float] = None

class DiscrepancyItem(BaseModel):
    id: str
    field: str
    discrepancy_type: str
    documents: List[DiscrepancyDocument] = Field(default_factory=list)
    values: Optional[List[Optional[str]]] = None
    normalized_values: Optional[List[Optional[str]]] = None
    comparison_status: Optional[str] = None
    difference: Optional[float] = None
    percentage_difference: Optional[float] = None
    severity: str
    severity_reasons: Optional[List[str]] = None
    confidence: float
    confidence_factors: Optional[Dict[str, Any]] = None
    explanation: str
    metadata: Optional[Dict[str, Any]] = None
    
    # Legacy fields kept for backward compatibility with frontend/tests
    document_a: Optional[str] = None
    document_b: Optional[str] = None
    value_a: Optional[str] = None
    value_b: Optional[str] = None

class AnalysisSummary(BaseModel):
    documents_analyzed: int
    total_discrepancies: int
    critical: int
    high: Optional[int] = 0
    medium: Optional[int] = 0
    low: Optional[int] = 0
    # Legacy fields
    warning: Optional[int] = 0
    minor: Optional[int] = 0

class ProjectDetails(BaseModel):
    road_name: str
    package_id: str
    district: str
    state: str

class RecordGroupItem(BaseModel):
    group_id: str
    documents: List[Dict[str, str]] = Field(default_factory=list)
    discrepancies: List[DiscrepancyItem] = Field(default_factory=list)

class AnalysisResultResponse(BaseModel):
    analysis_id: str
    project: Optional[ProjectDetails] = None
    summary: AnalysisSummary
    discrepancies: List[DiscrepancyItem] = Field(default_factory=list)
    
    # New Phase 3 properties
    processing_status: Optional[str] = "success"
    documents_analyzed: Optional[int] = 0
    linked_record_groups: Optional[int] = 0
    record_groups: Optional[List[RecordGroupItem]] = None

class UploadResponse(BaseModel):
    success: bool
    analysis_id: str
    filename: str
    ocr_confidence: float
    extracted_fields: Dict[str, Any]
