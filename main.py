#!/usr/bin/env python3
"""Main entry point for py-solana-pay application"""

import uvicorn
from src.py_solana_pay.main import app


def main():
    """Main function to run the FastAPI application"""
    print("Starting py-solana-pay server...")
    print("🔥 Python implementation of Solana-Pay")
    print("💰 A blockchain payment system built on the Solana platform")
    print("🚀 Server starting at http://localhost:8000")
    print("📖 API docs available at http://localhost:8000/docs")
    
    uvicorn.run(
        "src.py_solana_pay.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
