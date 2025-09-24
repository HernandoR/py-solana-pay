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
    print("Hello from py-solana-pay!")
