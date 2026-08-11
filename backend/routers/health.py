"""
GET /health — basic liveness check.
"""

from fastapi import APIRouter

from backend.models import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")