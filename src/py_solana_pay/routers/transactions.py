"""Transaction management router"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.account import Account
from ..models.transaction import Transaction
from .auth import get_current_user

router = APIRouter()

# Dependency injection variables
db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)


class TransactionBase(BaseModel):
    transaction_type: str
    transaction_details: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    transaction_id: int
    transaction_date: datetime
    username: str

    class Config:
        from_attributes = True


@router.get("", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = db_dependency,
    current_user: Account = current_user_dependency,
):
    """Get user's transactions"""
    transactions = (
        db.query(Transaction)
        .filter(Transaction.username == current_user.username)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return transactions


@router.get("/all", response_model=List[TransactionResponse])
async def get_all_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = db_dependency,
    current_user: Account = current_user_dependency,
):
    """Get all transactions (admin only - for now just returns user's transactions)"""
    # TODO: Add admin role check
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: Session = db_dependency,
    current_user: Account = current_user_dependency,
):
    """Get transaction by ID"""
    transaction = (
        db.query(Transaction)
        .filter(Transaction.transaction_id == transaction_id)
        .first()
    )
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Users can only view their own transactions
    if transaction.username != current_user.username:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this transaction"
        )

    return transaction


@router.post("", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = db_dependency,
    current_user: Account = current_user_dependency,
):
    """Create new transaction"""
    db_transaction = Transaction(
        **transaction.dict(),
        username=current_user.username,
        transaction_date=datetime.utcnow(),
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
