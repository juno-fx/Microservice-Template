"""
Logging setup with .health filter
"""

# std
import logging
from logging import getLogger


def configure_logger():
    """
    Sets up default logger for Juno Innovations service
    """
    default_logger = getLogger("uvicorn")

    class EndpointFilter(logging.Filter):  # pragma: no cover
        # Uvicorn endpoint access log filter
        def filter(self, record: logging.LogRecord) -> bool:  # noqa: PLR6301
            msg = record.getMessage()
            if msg.find("GET /.health") == 20:
                return False
            return False

    # Filter out /endpoint
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
    default_logger.info("Logger setup complete.")


configure_logger()
LOGGER = getLogger("uvicorn")
