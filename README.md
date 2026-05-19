# BitcoinCurrencyConverter

A Bitcoin to fiat currency converter that fetches real-time exchange rates using public APIs.

## Features

- Convert Bitcoin (BTC) to major fiat currencies (USD, EUR, GBP, JPY, etc.)
- Real-time exchange rates via CoinDesk API
- Simple CLI interface

## Usage

```bash
# Convert 1 BTC to USD
python btc_converter.py 1 USD

# Convert 0.5 BTC to EUR
python btc_converter.py 0.5 EUR

# List supported currencies
python btc_converter.py --list
```

## Requirements

- Python 3.7+
- `requests` library
