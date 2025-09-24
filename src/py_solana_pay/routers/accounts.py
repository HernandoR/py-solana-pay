"""Account management router"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..models.account import Account
from .auth import get_current_user

router = APIRouter()


class AccountResponse(BaseModel):
    username: str
    email: str
    fullname: str
    wallet_key: str = None
    
    class Config:
        from_attributes = True


class AccountUpdate(BaseModel):
    email: str = None
    fullname: str = None
    wallet_key: str = None


@router.get("/", response_model=List[AccountResponse])
async def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all accounts (admin only)"""
    accounts = db.query(Account).offset(skip).limit(limit).all()
    return accounts


@router.get("/{username}", response_model=AccountResponse)
async def get_account(username: str, db: Session = Depends(get_db)):
    """Get account by username"""
    account = db.query(Account).filter(Account.username == username).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{username}", response_model=AccountResponse)
async def update_account(
    username: str, 
    account_update: AccountUpdate, 
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    """Update account information"""
    # Users can only update their own account
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="Not authorized to update this account")
    
    account = db.query(Account).filter(Account.username == username).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if account_update.email is not None:
        account.email = account_update.email
    if account_update.fullname is not None:
        account.fullname = account_update.fullname
    if account_update.wallet_key is not None:
        account.wallet_key = account_update.wallet_key
    
    db.commit()
    db.refresh(account)
    return account