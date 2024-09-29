# utils/logging_utils.py

"""Logging utilities for the MAS application."""

import logging
from utils.constants import LOGGING_LEVEL


def setup_logging():
    """Set up the logging configuration."""
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
