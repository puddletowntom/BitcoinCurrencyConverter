#!/usr/bin/env python3
"""
BitcoinCurrencyConverter — Real-time BTC to fiat currency conversion.

Fetches exchange rates from the CoinDesk API and converts Bitcoin amounts
to user-specified fiat currencies.
"""

import argparse
import sys
from typing import Optional

import requests


COINDESK_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
CURRENCY_NAMES = {
    "USD": "United States Dollar",
    "GBP": "British Pound Sterling",
    "EUR": "Euro",
    "JPY": "Japanese Yen",
    "BRL": "Brazilian Real",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "DKK": "Danish Krone",
    "HKD": "Hong Kong Dollar",
    "INR": "Indian Rupee",
    "ISK": "Icelandic Króna",
    "KRW": "South Korean Won",
    "MXN": "Mexican Peso",
    "NOK": "Norwegian Krone",
    "NZD": "New Zealand Dollar",
    "PHP": "Philippine Peso",
    "PLN": "Polish Zloty",
    "RUB": "Russian Ruble",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "THB": "Thai Baht",
    "TWD": "New Taiwan Dollar",
    "ZAR": "South African Rand",
}


def fetch_rates() -> dict:
    """Fetch current Bitcoin price index from CoinDesk."""
    resp = requests.get(COINDESK_URL, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_rate(bpi: dict, currency: str) -> Optional[float]:
    """Extract the rate for a given currency code from the BPI data."""
    info = bpi.get(currency.upper())
    if info is None:
        return None
    rate_str = info["rate"].replace(",", "")
    return float(rate_str)


def format_output(amount: float, currency: str, converted: float, rate: float) -> str:
    """Format the conversion result for display."""
    symbols = {
        "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
        "BRL": "R$", "CAD": "C$", "CNY": "¥", "KRW": "₩",
        "INR": "₹", "MXN": "Mex$", "RUB": "₽", "ZAR": "R",
    }
    sym = symbols.get(currency, "")
    return (
        f"  {amount:.8f} BTC = {sym}{converted:,.2f} {currency}\n"
        f"  Rate: 1 BTC = {sym}{rate:,.2f} {currency}"
    )


def list_currencies() -> None:
    """Display all supported currencies."""
    print("Supported currencies:\n")
    for code, name in sorted(CURRENCY_NAMES.items()):
        print(f"  {code:>4s}  —  {name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Bitcoin to fiat currency",
    )
    parser.add_argument("amount", type=float, nargs="?", help="BTC amount to convert")
    parser.add_argument("currency", nargs="?", help="Target fiat currency code (e.g. USD, EUR)")
    parser.add_argument("--list", action="store_true", help="List supported currencies")
    args = parser.parse_args()

    if args.list:
        list_currencies()
        return

    if not args.amount or not args.currency:
        parser.print_help()
        sys.exit(1)

    currency = args.currency.upper()

    if currency not in CURRENCY_NAMES:
        print(f"Error: unsupported currency '{args.currency}'")
        print("Use --list to see supported currencies.")
        sys.exit(1)

    try:
        data = fetch_rates()
    except requests.RequestException as e:
        print(f"Error fetching rates: {e}", file=sys.stderr)
        sys.exit(1)

    rate = get_rate(data["bpi"], currency)
    if rate is None:
        print(f"Error: rate not available for {currency}", file=sys.stderr)
        sys.exit(1)

    converted = args.amount * rate
    print(format_output(args.amount, currency, converted, rate))
    print(f"\n  Updated: {data['time']['updated']}")


if __name__ == "__main__":
    main()
