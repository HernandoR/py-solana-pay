"""
Python implementation of Solana-Pay

A blockchain payment system built on the Solana platform, focusing on improving
security and privacy in transactions.
"""

try:
    from .main import app
except ImportError:
    # Handle import errors gracefully during development
    app = None

__version__ = "0.1.0"

__all__ = ["app"]


def main() -> None:
    """Main entry point for the application"""
    import uvicorn

    from .logging_config import get_logger, log_app_event
    from .main import app
    
    logger = get_logger(__name__)

    logger.info("🔥 py-solana-pay Server")
    logger.info("💰 Python implementation of Solana-Pay")
    logger.info("🚀 Starting at http://localhost:8000")
    logger.info("📖 API docs at http://localhost:8000/docs")
    
    log_app_event("Application main entry point called")

    uvicorn.run("py_solana_pay.main:app", host="0.0.0.0", port=8000, reload=True)
