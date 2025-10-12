#!/usr/bin/env python3
"""Main entry point for py-solana-pay application"""

import uvicorn

from src.py_solana_pay.logging_config import get_logger, log_app_event

logger = get_logger(__name__)


def main():
    """Main function to run the FastAPI application"""
    logger.info("Starting py-solana-pay server...")
    logger.info("🔥 Python implementation of Solana-Pay")
    logger.info("💰 A blockchain payment system built on the Solana platform")
    logger.info("🚀 Server starting at http://localhost:8000")
    logger.info("📖 API docs available at http://localhost:8000/docs")

    log_app_event("Server startup initiated")

    uvicorn.run(
        "src.py_solana_pay.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
