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


        print("🔥 py-solana-pay Server")
        print("💰 Python implementation of Solana-Pay")
        print("🚀 Starting at http://localhost:8000")
        print("📖 API docs at http://localhost:8000/docs")

        uvicorn.run("py_solana_pay.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
