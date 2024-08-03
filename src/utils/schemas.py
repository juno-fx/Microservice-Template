"""
Utility endpoints for service health checks and other misc. tasks
"""

# 3rd
from pydantic import BaseModel


class HealthCheck(BaseModel):
    """
    Response model to validate and return when performing a health check.
    """

    status: str = "OK"
