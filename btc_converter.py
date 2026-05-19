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


BLOCKCHAIN_API = "https://blockchain.info/ticker"
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

CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
    "BRL": "R$", "CAD": "C$", "CNY": "¥", "KRW": "₩",
    "INR": "₹", "MXN": "Mex$", "RUB": "₽", "ZAR": "R",
    "ARS": "$", "AUD": "A$", "CLP": "$", "COP": "$",
    "DKK": "kr", "HKD": "HK$", "ILS": "₪", "ISK": "kr",
    "KRW": "₩", "NOK": "kr", "NZD": "NZ$", "PEN": "S/",
    "PHP": "₱", "PLN": "zł", "SEK": "kr", "SGD": "S$",
    "THB": "฿", "TWD": "NT$", "UYU": "$U", "VEF": "Bs",
}


def fetch_rates() -> dict:
    """Fetch current BTC/fiat rates from Blockchain.info."""
    resp = requests.get(BLOCKCHAIN_API, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_rate(ticker: dict, currency: str) -> Optional[float]:
    """Extract the last (sell) rate for a given currency code."""
    info = ticker.get(currency.upper())
    if info is None:
        return None
    return float(info["last"])


def format_output(amount: float, currency: str, converted: float, rate: float) -> str:
    """Format the conversion result for display."""
    sym = CURRENCY_SYMBOLS.get(currency, "")
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

    rate = get_rate(data, currency)
    if rate is None:
        print(f"Error: rate not available for {currency}", file=sys.stderr)
        sys.exit(1)

    converted = args.amount * rate
    print(format_output(args.amount, currency, converted, rate))


if __name__ == "__main__":
    main()
