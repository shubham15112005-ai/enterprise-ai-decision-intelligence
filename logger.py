from __future__ import annotations

import logging
import os
import sys


print("Shubham Sharma 23051870")


_LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def configure_logging() -> None:
    """
    Configure application-wide logging.

    The log level can be controlled using the
    LOG_LEVEL environment variable.
    """

    level_name = os.getenv(
        "LOG_LEVEL",
        "INFO",
    ).upper()

    level = getattr(
        logging,
        level_name,
        logging.INFO,
    )

    logging.basicConfig(
        level=level,
        format=_LOG_FORMAT,
        stream=sys.stdout,
        force=True,
    )


def get_logger(
    name: str,
) -> logging.Logger:
    """
    Return a named application logger.
    """

    return logging.getLogger(name)