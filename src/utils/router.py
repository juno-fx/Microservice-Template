"""
Utility endpoints for service health checks and other misc. tasks
"""

# 3rd
from fastapi import APIRouter, status

# local
from .schemas import HealthCheck


router = APIRouter(tags=["Utility"])


@router.get("/.health", response_model=HealthCheck, status_code=status.HTTP_200_OK)
def handler() -> HealthCheck:  # pragma: no cover
    """
    Return a health check response
    """
    return HealthCheck(status="OK")
