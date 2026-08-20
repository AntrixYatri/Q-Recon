from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AnalysisRequest(BaseModel):
    analysis_id: str = Field(..., description="The unique ID of the project/road to analyze")
    documents: Optional[List[Dict[str, Any]]] = Field(
        default=None, 
        description="Optional list of mixed documents to analyze (raw path dicts or structured bypass data)"
    )

class ProjectMeta(BaseModel):
    road_name: Optional[str] = ""
    package_id: Optional[str] = ""
    district: Optional[str] = ""
    state: Optional[str] = ""
