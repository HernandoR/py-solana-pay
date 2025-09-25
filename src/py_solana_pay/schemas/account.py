"""Account-related Pydantic schemas"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    fullname: str = Field(..., min_length=1, max_length=100, description="Full name")
    password: str = Field(..., min_length=6, description="Password")
    wallet_key: Optional[str] = Field(None, description="Solana wallet public key")


class UserResponse(BaseModel):
    username: str
    email: str
    fullname: str
    wallet_key: Optional[str] = None

    class Config:
        from_attributes = True


class AccountUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Email address")
    fullname: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Full name"
    )
    wallet_key: Optional[str] = Field(None, description="Solana wallet public key")


class AccountResponse(BaseModel):
    username: str
    email: str
    fullname: str
    wallet_key: Optional[str] = None

    class Config:
        from_attributes = True
