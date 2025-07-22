# dahua_ipc/logging_config.py

import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name='dahua_ipc', log_file='dahua_ipc.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Prevent duplicate logs in root

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_format = logging.Formatter("[%(levelname)s] %(message)s")
        console_handler.setFormatter(console_format)

        # File handler with rotation
        file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=2)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
