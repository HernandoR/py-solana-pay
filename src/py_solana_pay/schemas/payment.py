"""Payment-related Pydantic schemas"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    recipient: str = Field(..., description="Solana wallet address of the recipient")
    amount: float = Field(..., gt=0, description="Payment amount")
    label: Optional[str] = Field(None, description="Payment label")
    message: Optional[str] = Field(None, description="Payment message")
    memo: Optional[str] = Field(None, description="Payment memo")


class PaymentUrlResponse(BaseModel):
    payment_url: str = Field(..., description="Generated Solana Pay URL")
    qr_code_url: Optional[str] = Field(None, description="QR code URL for the payment")


class CheckoutItem(BaseModel):
    name: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class CheckoutSessionRequest(BaseModel):
    items: List[CheckoutItem] = Field(..., description="Items to purchase")
    success_url: str = Field(..., description="URL to redirect on successful payment")
    cancel_url: str = Field(..., description="URL to redirect on cancelled payment") 
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class CheckoutSessionResponse(BaseModel):
    session_id: str
    order_id: str
    checkout_url: Optional[str] = None


class PaymentVerificationRequest(BaseModel):
    signature: str = Field(..., description="Solana transaction signature")
    expected_amount: Optional[float] = Field(None, description="Expected payment amount")
    expected_recipient: Optional[str] = Field(None, description="Expected recipient address")


class PaymentVerificationResponse(BaseModel):
    verified: bool
    signature: str
    amount: Optional[float] = None
    recipient: Optional[str] = None
    timestamp: Optional[str] = None
    message: str