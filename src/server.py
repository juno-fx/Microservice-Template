"""
Server handler
"""

# std
import os
from logging import getLogger

# 3rd
from fastapi import FastAPI

# local
from .startup import startup
from .logger import configure_logger
from .header import header
from .utils import router as utils

# globals
LOGGER = getLogger("uvicorn")
COMMIT = os.environ.get("COMMIT", "unknown")
version = f"v0.0.0 build@{COMMIT[len(COMMIT) - 7:]}"

app = FastAPI(
    title="Juno Service",
    version=version,
    summary="Juno API",
    description="New Juno Service",
    redoc_url=None,
)

header(LOGGER, version, "Juno Service")

app.include_router(utils)


@app.on_event("startup")
def _startup():  # pragma: no cover
    """
    Initial setup
    """
    configure_logger()
    startup()
