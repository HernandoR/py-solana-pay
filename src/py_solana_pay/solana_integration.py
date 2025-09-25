"""Solana blockchain integration utilities"""

import base64 as b64
from io import BytesIO
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import qrcode
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.signature import Signature


class SolanaPayUtil:
    """Utility class for Solana Pay operations"""

    def __init__(self, rpc_url: str = "https://api.mainnet-beta.solana.com"):
        self.client = Client(rpc_url)

    def generate_payment_url(
        self,
        recipient: str,
        amount: float,
        spl_token: Optional[str] = None,
        reference: Optional[str] = None,
        label: Optional[str] = None,
        message: Optional[str] = None,
        memo: Optional[str] = None,
    ) -> str:
        """
        Generate a Solana Pay URL following the specification
        https://docs.solanapay.com/spec
        """
        # Validate recipient address
        try:
            Pubkey.from_string(recipient)
        except Exception as e:
            raise ValueError("Invalid recipient address") from e

        # Build URL parameters
        params = {}

        if amount > 0:
            params["amount"] = str(amount)

        if spl_token:
            params["spl-token"] = spl_token

        if reference:
            params["reference"] = reference

        if label:
            params["label"] = label

        if message:
            params["message"] = message

        if memo:
            params["memo"] = memo

        # Construct the URL
        base_url = f"solana:{recipient}"
        if params:
            base_url += "?" + urlencode(params)

        return base_url

    def generate_qr_code(self, payment_url: str) -> str:
        """Generate QR code for payment URL and return as base64 string"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(payment_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64 string
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = b64.b64encode(buffered.getvalue()).decode()

        return f"data:image/png;base64,{img_str}"

    def verify_transaction(
        self,
        signature: str,
        expected_recipient: Optional[str] = None,
        expected_amount: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Verify a Solana transaction
        Returns transaction details if valid
        """
        try:
            # Parse signature
            sig = Signature.from_string(signature)

            # Get transaction details
            response = self.client.get_transaction(sig)

            if not response.value:
                return {"verified": False, "error": "Transaction not found"}

            tx_info = response.value

            # Basic verification - transaction exists and succeeded
            if tx_info.meta.err:
                return {
                    "verified": False,
                    "error": f"Transaction failed: {tx_info.meta.err}",
                }

            # Extract transaction details
            result = {
                "verified": True,
                "signature": signature,
                "slot": tx_info.slot,
                "block_time": tx_info.block_time,
                "fee": tx_info.meta.fee,
                "pre_balances": tx_info.meta.pre_balances,
                "post_balances": tx_info.meta.post_balances,
            }

            # Additional verification if expected values provided
            if expected_recipient or expected_amount:
                # This would require parsing the transaction instructions
                # to verify the actual transfer details
                # For now, just return basic verification
                pass

            return result

        except Exception as e:
            return {"verified": False, "error": f"Verification failed: {str(e)}"}

    def get_account_balance(self, address: str) -> Optional[float]:
        """Get SOL balance for an account"""
        try:
            pubkey = Pubkey.from_string(address)
            response = self.client.get_balance(pubkey)

            if response.value is not None:
                # Convert lamports to SOL (1 SOL = 1e9 lamports)
                return response.value / 1e9

        except Exception as e:
            print(f"Error getting balance: {e}")

        return None


# Global instance
solana_pay = SolanaPayUtil()
