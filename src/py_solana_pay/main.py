"""Main FastAPI application"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import get_db, engine, Base

# Import models to ensure tables are created
from .models.account import Account
from .models.product import Product 
from .models.transaction import Transaction
from .models.bank_account import BankAccount
from .models.authorities import Authorities
from .models.role import Role
from .models.comment import Comment
from .models.reply import Reply

# Import routers
from .routers import accounts, products, transactions, checkout, auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="py-solana-pay",
    description="Python implementation of Solana-Pay - A blockchain payment system",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(checkout.router, prefix="/api/checkout", tags=["checkout"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to py-solana-pay!",
        "description": "Python implementation of Solana-Pay - A blockchain payment system",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)