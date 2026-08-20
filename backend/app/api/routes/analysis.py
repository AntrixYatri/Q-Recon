from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import AnalysisRequest
from app.models.response_models import AnalysisResultResponse
from app.services.analysis_service import AnalysisService
from app.services.report_service import ReportService

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResultResponse)
async def run_analysis(request: AnalysisRequest):
    """
    Triggers the comparative discrepancy detection engine across a project's quality documents.
    """
    try:
        # Run comparison and fetch results
        results = AnalysisService.run_analysis(request.analysis_id)
        
        # Save results log
        ReportService.save_analysis_result(request.analysis_id, results)
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discrepancy audit failed: {str(e)}")

@router.get("/results/{analysis_id}", response_model=AnalysisResultResponse)
async def get_results(analysis_id: str):
    """
    Retrieve the generated discrepancy report and confidence ratings for a project.
    """
    try:
        results = ReportService.get_analysis_result(analysis_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Analysis results for '{analysis_id}' not found: {str(e)}")
