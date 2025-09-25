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

    from .main import app

    print("🔥 py-solana-pay Server")
    print("💰 Python implementation of Solana-Pay")
    print("🚀 Starting at http://localhost:8000")
    print("📖 API docs at http://localhost:8000/docs")

    uvicorn.run("py_solana_pay.main:app", host="0.0.0.0", port=8000, reload=True)
