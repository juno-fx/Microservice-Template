"""
Juno Innovations Header
"""

import os
import locale


def header(logger, version, service):
    """
    Print the header of the service
    """
    logger.info("")
    # pylint: disable=unspecified-encoding
    with open(
        os.path.abspath(f"{__file__}/../juno-ascii.txt"),
        "r",
        encoding=locale.getpreferredencoding(False),
    ) as fetch:
        for line in fetch.readlines():
            logger.info(line.rstrip())
    logger.info("")
    logger.info("JUNO INNOVATIONS")
    logger.info(f"{service} API Server: {version}")
    logger.info("")
