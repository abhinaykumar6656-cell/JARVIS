"""
=========================================================
JARVIS Logging Engine
=========================================================

Provides centralized logging for the entire application.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings

# --------------------------------------------------
# Create logs directory if it doesn't exist
# --------------------------------------------------

LOG_PATH = Path(settings.LOG_FILE)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Log format
# --------------------------------------------------

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | "
    "%(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# --------------------------------------------------
# Configure logger
# --------------------------------------------------

logger = logging.getLogger(settings.APP_NAME)
logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

# Prevent duplicate logs
logger.propagate = False

# --------------------------------------------------
# Console Handler
# --------------------------------------------------

console_handler = logging.StreamHandler()

console_handler.setFormatter(
    logging.Formatter(LOG_FORMAT, DATE_FORMAT)
)

# --------------------------------------------------
# File Handler
# --------------------------------------------------

file_handler = RotatingFileHandler(
    filename=settings.LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5,
    encoding="utf-8",
)

file_handler.setFormatter(
    logging.Formatter(LOG_FORMAT, DATE_FORMAT)
)

# --------------------------------------------------
# Attach handlers only once
# --------------------------------------------------

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)