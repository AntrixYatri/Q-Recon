from fastapi import APIRouter
from app.models.response_models import HealthResponse

router = APIRouter()

@router.get("", response_model=HealthResponse)
async def get_health():
    """
    Check the health status of the QCR AI backend.
    """
    return HealthResponse(status="ok", service="QCR AI Core Pipeline")
