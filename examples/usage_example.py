"""
Example usage of py-solana-pay API

This script demonstrates how to:
1. Register a new user
2. Login and get an access token
3. Create a product
4. Generate a Solana payment URL
5. Verify a payment
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel, EmailStr, Field, field_validator

# Add src to path to import logging_config
sys.path.append(str(Path(__file__).parent.parent / "src"))
from py_solana_pay.logging_config import get_logger

logger = get_logger(__name__)

BASE_URL = "http://localhost:8000"


# Pydantic models for request validation
class UserRegistration(BaseModel):
    """Model for user registration request"""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    fullname: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)
    wallet_key: Optional[str] = Field(None, min_length=32, max_length=44)

    @field_validator("wallet_key")
    @classmethod
    def validate_wallet_key(cls, v: Optional[str]) -> Optional[str]:
        """Validate Solana wallet address format (base58)"""
        if v is None:
            return v
        # Basic validation for Solana address (base58, 32-44 characters)
        import re

        if not re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", v):
            raise ValueError("Invalid Solana wallet address format")
        return v


class LoginCredentials(BaseModel):
    """Model for login credentials"""

    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)


class ProductCreate(BaseModel):
    """Model for product creation request"""

    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=1, ge=1)
    image: Optional[str] = None


class PaymentURLRequest(BaseModel):
    """Model for payment URL generation request"""

    recipient: str = Field(..., min_length=32, max_length=44)
    amount: float = Field(..., gt=0)
    label: Optional[str] = Field(None, max_length=100)
    message: Optional[str] = Field(None, max_length=500)

    @field_validator("recipient")
    @classmethod
    def validate_recipient(cls, v: str) -> str:
        """Validate recipient is a valid Solana address"""
        import re

        if not re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", v):
            raise ValueError("Invalid Solana wallet address format")
        return v


class SolanaPayClient:
    """Client for interacting with py-solana-pay API using httpx"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.client = httpx.Client(timeout=30.0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def close(self):
        """Close the HTTP client"""
        self.client.close()

    def register_user(
        self,
        username: str,
        email: str,
        fullname: str,
        password: str,
        wallet_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Register a new user with validated parameters"""
        # Validate input using Pydantic
        registration = UserRegistration(
            username=username,
            email=email,
            fullname=fullname,
            password=password,
            wallet_key=wallet_key,
        )

        response = self.client.post(
            f"{self.base_url}/api/auth/register",
            json=registration.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return response.json()

    def login(self, username: str, password: str) -> str:
        """Login and get access token with validated credentials"""
        # Validate credentials using Pydantic
        credentials = LoginCredentials(username=username, password=password)

        response = self.client.post(
            f"{self.base_url}/api/auth/token",
            data=credentials.model_dump(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()

        token_data = response.json()
        self.token = token_data["access_token"]
        return self.token

    def _headers(self) -> Dict[str, str]:
        """Get headers with authorization"""
        if not self.token:
            raise ValueError("Not authenticated. Call login() first.")

        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def create_product(
        self, name: str, price: float, quantity: int = 1, image: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new product with validated parameters"""
        # Validate product data using Pydantic
        product = ProductCreate(name=name, price=price, quantity=quantity, image=image)

        response = self.client.post(
            f"{self.base_url}/api/products/",
            json=product.model_dump(exclude_none=True),
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def generate_payment_url(
        self,
        recipient: str,
        amount: float,
        label: Optional[str] = None,
        message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a Solana payment URL with validated parameters"""
        # Validate payment request using Pydantic
        payment_request = PaymentURLRequest(
            recipient=recipient, amount=amount, label=label, message=message
        )

        response = self.client.post(
            f"{self.base_url}/api/checkout/payment-url",
            json=payment_request.model_dump(exclude_none=True),
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def get_transactions(self) -> List[Dict[str, Any]]:
        """Get user's transactions"""
        response = self.client.get(
            f"{self.base_url}/api/transactions/", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()


def main():
    """Example usage"""
    with SolanaPayClient() as client:
        print("🔥 py-solana-pay Example Usage")  # Keep CLI output
        print("=" * 40)
        logger.info("Starting py-solana-pay example usage demonstration")

        # 1. Register a user
        print("1. Registering user...")
        logger.info("Attempting to register demo user")
        try:
            user = client.register_user(
                username="demo_user",
                email="demo@example.com",
                fullname="Demo User",
                password="secure_password123",
                wallet_key="11111111111111111111111111111112",  # System program address (valid)
            )
            print(f"✅ User registered: {user['username']}")
            logger.info(f"User registered successfully: {user['username']}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                print("ℹ️  User already exists, continuing...")
                logger.info("User already exists, continuing with demo")
            else:
                logger.error(f"Failed to register user: {e}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error during registration: {e}")
            raise

        # 2. Login
        print("\n2. Logging in...")
        logger.info("Attempting to login user")
        try:
            token = client.login("demo_user", "secure_password123")  # noqa
            print("✅ Logged in successfully")
            logger.info("User logged in successfully")
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to login: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            raise

        # 3. Create a product
        print("\n3. Creating a product...")
        logger.info("Creating demo product")
        try:
            product = client.create_product(
                name="Digital Art NFT",
                price=0.5,  # 0.5 SOL
                quantity=1,
                image="https://example.com/nft.png",
            )
            print(f"✅ Product created: {product['name']} (ID: {product['id']})")
            logger.info(f"Product created: {product['name']} (ID: {product['id']})")
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to create product: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during product creation: {e}")
            raise

        # 4. Generate payment URL
        print("\n4. Generating payment URL...")
        logger.info("Generating demo payment URL")
        try:
            payment = client.generate_payment_url(
                recipient="11111111111111111111111111111112",
                amount=0.1,
                label="py-solana-pay Demo",
                message="Demo payment for testing",
            )
            print(f"✅ Payment URL: {payment['payment_url']}")
            print(f"✅ QR Code available: {'qr_code_url' in payment}")
            logger.info(f"Generated payment URL: {payment['payment_url']}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to generate payment URL: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during payment URL generation: {e}")
            raise

        # 5. Get transactions
        print("\n5. Fetching transactions...")
        logger.info("Fetching transaction history")
        try:
            transactions = client.get_transactions()
            print(f"✅ Found {len(transactions)} transactions")
            logger.info(f"Retrieved {len(transactions)} transactions")

            for tx in transactions[-3:]:  # Show last 3 transactions
                print(
                    f"   - {tx['transaction_type']}: {tx['transaction_details'][:50]}..."
                )
                logger.debug(
                    f"Transaction: {tx['transaction_type']} - {tx['transaction_details'][:50]}..."
                )
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to fetch transactions: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during transaction fetching: {e}")
            raise

        print("\n🎉 Example completed successfully!")
        print(
            "\nTo try payment verification, you would need a real Solana transaction signature."
        )
        print("The API is ready to handle real Solana payments!")
        logger.info("Example usage completed successfully")


if __name__ == "__main__":
    main()
