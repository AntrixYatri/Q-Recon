from pydantic import BaseModel, Field
from typing import Optional, List

class AnalysisRequest(BaseModel):
    analysis_id: str = Field(..., description="The unique ID of the project/road to analyze")

class ProjectMeta(BaseModel):
    road_name: Optional[str] = ""
    package_id: Optional[str] = ""
    district: Optional[str] = ""
    state: Optional[str] = ""
