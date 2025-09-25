#!/usr/bin/env python3
"""
CLI tool for py-solana-pay

Usage:
    python -m py_solana_pay.cli generate-url --recipient <address> --amount <amount>
    python -m py_solana_pay.cli verify --signature <signature>
    python -m py_solana_pay.cli balance --address <address>
"""

import argparse
import sys

from .solana_integration import solana_pay


def generate_payment_url(args):
    """Generate a Solana payment URL"""
    try:
        url = solana_pay.generate_payment_url(
            recipient=args.recipient,
            amount=args.amount,
            label=args.label,
            message=args.message,
            memo=args.memo,
        )

        print(f"Payment URL: {url}")

        if args.qr:
            qr_data = solana_pay.generate_qr_code(url)
            print(f"QR Code: {qr_data}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def verify_payment(args):
    """Verify a Solana payment"""
    try:
        result = solana_pay.verify_transaction(
            signature=args.signature,
            expected_recipient=args.expected_recipient,
            expected_amount=args.expected_amount,
        )

        if result["verified"]:
            print("✅ Payment verified successfully!")
            print(f"Signature: {args.signature}")
            if "block_time" in result:
                print(f"Block time: {result['block_time']}")
            if "fee" in result:
                print(f"Fee: {result['fee']} lamports")
        else:
            print("❌ Payment verification failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def get_balance(args):
    """Get wallet balance"""
    try:
        balance = solana_pay.get_account_balance(args.address)

        if balance is not None:
            print(f"Address: {args.address}")
            print(f"Balance: {balance} SOL")
        else:
            print(f"Could not retrieve balance for {args.address}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="py-solana-pay CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate URL command
    url_parser = subparsers.add_parser(
        "generate-url", help="Generate Solana payment URL"
    )
    url_parser.add_argument(
        "--recipient", required=True, help="Recipient wallet address"
    )
    url_parser.add_argument(
        "--amount", type=float, required=True, help="Payment amount in SOL"
    )
    url_parser.add_argument("--label", help="Payment label")
    url_parser.add_argument("--message", help="Payment message")
    url_parser.add_argument("--memo", help="Payment memo")
    url_parser.add_argument("--qr", action="store_true", help="Generate QR code")

    # Verify payment command
    verify_parser = subparsers.add_parser("verify", help="Verify Solana payment")
    verify_parser.add_argument(
        "--signature", required=True, help="Transaction signature"
    )
    verify_parser.add_argument(
        "--expected-recipient", help="Expected recipient address"
    )
    verify_parser.add_argument("--expected-amount", type=float, help="Expected amount")

    # Balance command
    balance_parser = subparsers.add_parser("balance", help="Get wallet balance")
    balance_parser.add_argument("--address", required=True, help="Wallet address")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "generate-url":
        generate_payment_url(args)
    elif args.command == "verify":
        verify_payment(args)
    elif args.command == "balance":
        get_balance(args)


if __name__ == "__main__":
    main()
