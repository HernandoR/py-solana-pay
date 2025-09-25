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
from typing import Any, Dict, List

import requests

# Add src to path to import logging_config
sys.path.append(str(Path(__file__).parent.parent / "src"))
from py_solana_pay.logging_config import get_logger

logger = get_logger(__name__)

BASE_URL = "http://localhost:8000"


class SolanaPayClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token = None

    def register_user(
        self,
        username: str,
        email: str,
        fullname: str,
        password: str,
        wallet_key: str = None,
    ) -> Dict[str, Any]:
        """Register a new user"""
        data = {
            "username": username,
            "email": email,
            "fullname": fullname,
            "password": password,
            "wallet_key": wallet_key,
        }

        response = requests.post(f"{self.base_url}/api/auth/register", json=data)
        response.raise_for_status()
        return response.json()

    def login(self, username: str, password: str) -> str:
        """Login and get access token"""
        data = {"username": username, "password": password}

        response = requests.post(
            f"{self.base_url}/api/auth/token",
            data=data,
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
        self, name: str, price: float, quantity: int = 1, image: str = None
    ) -> Dict[str, Any]:
        """Create a new product"""
        data = {"name": name, "price": price, "quantity": quantity, "image": image}

        response = requests.post(
            f"{self.base_url}/api/products/", json=data, headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def generate_payment_url(
        self, recipient: str, amount: float, label: str = None, message: str = None
    ) -> Dict[str, Any]:
        """Generate a Solana payment URL"""
        data = {
            "recipient": recipient,
            "amount": amount,
            "label": label,
            "message": message,
        }

        response = requests.post(
            f"{self.base_url}/api/checkout/payment-url",
            json=data,
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def get_transactions(self) -> List[Dict[str, Any]]:
        """Get user's transactions"""
        response = requests.get(
            f"{self.base_url}/api/transactions/", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()


def main():
    """Example usage"""
    client = SolanaPayClient()

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
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print("ℹ️  User already exists, continuing...")
            logger.info("User already exists, continuing with demo")
        else:
            logger.error(f"Failed to register user: {e}")
            raise

    # 2. Login
    print("\n2. Logging in...")
    logger.info("Attempting to login user")
    token = client.login("demo_user", "secure_password123")  # noqa
    print("✅ Logged in successfully")
    logger.info("User logged in successfully")

    # 3. Create a product
    print("\n3. Creating a product...")
    logger.info("Creating demo product")
    product = client.create_product(
        name="Digital Art NFT",
        price=0.5,  # 0.5 SOL
        quantity=1,
        image="https://example.com/nft.png",
    )
    print(f"✅ Product created: {product['name']} (ID: {product['id']})")
    logger.info(f"Product created: {product['name']} (ID: {product['id']})")

    # 4. Generate payment URL
    print("\n4. Generating payment URL...")
    logger.info("Generating demo payment URL")
    payment = client.generate_payment_url(
        recipient="11111111111111111111111111111112",
        amount=0.1,
        label="py-solana-pay Demo",
        message="Demo payment for testing",
    )
    print(f"✅ Payment URL: {payment['payment_url']}")
    print(f"✅ QR Code available: {'qr_code_url' in payment}")
    logger.info(f"Generated payment URL: {payment['payment_url']}")

    # 5. Get transactions
    print("\n5. Fetching transactions...")
    logger.info("Fetching transaction history")
    transactions = client.get_transactions()
    print(f"✅ Found {len(transactions)} transactions")
    logger.info(f"Retrieved {len(transactions)} transactions")

    for tx in transactions[-3:]:  # Show last 3 transactions
        print(f"   - {tx['transaction_type']}: {tx['transaction_details'][:50]}...")
        logger.debug(f"Transaction: {tx['transaction_type']} - {tx['transaction_details'][:50]}...")

    print("\n🎉 Example completed successfully!")
    print(
        "\nTo try payment verification, you would need a real Solana transaction signature."
    )
    print("The API is ready to handle real Solana payments!")
    logger.info("Example usage completed successfully")


if __name__ == "__main__":
    main()
