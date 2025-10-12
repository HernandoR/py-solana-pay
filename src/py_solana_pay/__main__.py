#!/usr/bin/env python3
"""Entry point for py-solana-pay when run as module"""

import sys


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        # Run CLI
        from .cli import main as cli_main

        sys.argv = sys.argv[1:]  # Remove 'cli' from args
        cli_main()
    else:
        # Run server
        import uvicorn

        from .logging_config import get_logger, log_app_event

        logger = get_logger(__name__)

        logger.info("🔥 py-solana-pay Server")
        logger.info("💰 Python implementation of Solana-Pay")
        logger.info("🚀 Starting at http://localhost:8000")
        logger.info("📖 API docs at http://localhost:8000/docs")

        log_app_event("Module main entry point called")

        uvicorn.run("py_solana_pay.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
