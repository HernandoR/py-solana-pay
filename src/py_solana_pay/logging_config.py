"""
Logging configuration for py-solana-pay using loguru
"""

import os
import sys

from loguru import logger

# Remove default logger
logger.remove()

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure console logging
logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    colorize=True,
    enqueue=True,
)

# Configure file logging - general log
logger.add(
    "logs/py_solana_pay.log",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="30 days",
    compression="gz",
    enqueue=True,
)

# Configure file logging - error log
logger.add(
    "logs/py_solana_pay_errors.log",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="10 MB",
    retention="30 days",
    compression="gz",
    enqueue=True,
)

# Configure file logging - application events
logger.add(
    "logs/py_solana_pay_app.log",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="gz",
    enqueue=True,
    filter=lambda record: record["level"].no >= logger.level("INFO").no
    and "app_event" in record["extra"],
)


def get_logger(name: str = None):
    """
    Get a logger instance for the specified module.

    Args:
        name: Module name for the logger

    Returns:
        Logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger


def log_app_event(message: str, level: str = "INFO"):
    """
    Log application-specific events to the app log file.

    Args:
        message: Message to log
        level: Log level (INFO, WARNING, ERROR, etc.)
    """
    logger.bind(app_event=True).log(level, message)
