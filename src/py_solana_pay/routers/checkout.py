"""Checkout and payment processing router"""

from typing import Any, Dict

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db, settings
from ..models.account import Account
from ..models.transaction import Transaction
from ..schemas.payment import (
    PaymentRequest,
    PaymentUrlResponse,
    PaymentVerificationRequest,
    PaymentVerificationResponse,
)
from ..solana_integration import solana_pay
from .auth import get_current_user

router = APIRouter()

# Dependency injection variables
db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)


@router.post("/session", response_model=Dict[str, str])
async def create_checkout_session(
    request_data: Dict[str, Any],
    db: Session = db_dependency,
    current_user: Account = current_user_dependency,
):
    """Create a checkout session with CandyPay"""

    if not settings.candypay_private_api_key:
        raise HTTPException(status_code=500, detail="CandyPay API key not configured")

    headers = {
        "Authorization": f"Bearer {settings.candypay_private_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.candypay_endpoint}/session",
                json=request_data,
                headers=headers,
                timeout=30.0,
            )
            response.raise_for_status()
            response_data = response.json()

            # Create a transaction record
            transaction = Transaction(
                transaction_type="CHECKOUT_SESSION",
                transaction_details=f"Session ID: {response_data.get('session_id')}, Order ID: {response_data.get('order_id')}",
                username=current_user.username,
            )
            db.add(transaction)
            db.commit()

            return {
                "session_id": response_data.get("session_id"),
                "order_id": response_data.get("order_id"),
            }

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Payment provider error: {str(e)}") from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Checkout session creation failed: {str(e)}"
        ) from e


@router.post("/payment-url", response_model=PaymentUrlResponse)
async def create_payment_url(
    payment_request: PaymentRequest,
    db: Session = db_dependency,
    current_user: Account = current_user_dependency,
):
    """Generate Solana payment URL with QR code"""

    try:
        # Generate Solana Pay URL
        payment_url = solana_pay.generate_payment_url(
            recipient=payment_request.recipient,
            amount=payment_request.amount,
            label=payment_request.label,
            message=payment_request.message,
            memo=payment_request.memo,
        )

        # Generate QR code
        qr_code_data = solana_pay.generate_qr_code(payment_url)

        # Record the payment URL generation
        transaction = Transaction(
            transaction_type="PAYMENT_URL_GENERATED",
            transaction_details=f"Payment URL generated for amount: {payment_request.amount} SOL to {payment_request.recipient}",
            username=current_user.username,
        )
        db.add(transaction)
        db.commit()

        return PaymentUrlResponse(payment_url=payment_url, qr_code_url=qr_code_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Payment URL generation failed: {str(e)}"
        ) from e


@router.post("/verify-payment", response_model=PaymentVerificationResponse)
async def verify_payment(
    verification_request: PaymentVerificationRequest,
    db: Session = db_dependency,
    current_user: Account = current_user_dependency,
):
    """Verify Solana payment signature"""

    try:
        # Verify the transaction on Solana blockchain
        verification_result = solana_pay.verify_transaction(
            signature=verification_request.signature,
            expected_recipient=verification_request.expected_recipient,
            expected_amount=verification_request.expected_amount,
        )

        # Record the verification attempt
        transaction = Transaction(
            transaction_type="PAYMENT_VERIFICATION",
            transaction_details=f"Verification for signature: {verification_request.signature[:20]}... - Result: {verification_result.get('verified', False)}",
            username=current_user.username,
        )
        db.add(transaction)
        db.commit()

        return PaymentVerificationResponse(
            verified=verification_result.get("verified", False),
            signature=verification_request.signature,
            amount=verification_result.get("amount"),
            recipient=verification_result.get("recipient"),
            timestamp=str(verification_result.get("block_time"))
            if verification_result.get("block_time")
            else None,
            message=verification_result.get("error", "Payment verification completed"),
        )

    except Exception as e:
        return PaymentVerificationResponse(
            verified=False,
            signature=verification_request.signature,
            message=f"Verification failed: {str(e)}",
        )


@router.get("/balance/{address}")
async def get_wallet_balance(
    address: str, current_user: Account = current_user_dependency
):
    """Get SOL balance for a wallet address"""

    try:
        balance = solana_pay.get_account_balance(address)

        if balance is None:
            raise HTTPException(
                status_code=404, detail="Could not retrieve balance for this address"
            )

        return {"address": address, "balance": balance, "currency": "SOL"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Balance retrieval failed: {str(e)}"
        ) from e
