#!/usr/bin/env python3
"""
Test script for currency conversion functionality
"""

from models.assets import Asset
from models.portfolio import Portfolio
from utils.currency_converter import converter

def test_currency_conversion():
    print("Testing Currency Conversion...")

    # Test assets in different currencies
    assets = [
        Asset("AAPL", "stock", 1000, 1200, "USD"),  # $1000 invested, $1200 current
        Asset("TSLA", "stock", 50000, 60000, "INR"),  # ₹50000 invested, ₹60000 current
        Asset("BTC", "crypto", 0.5, 0.6, "BTC"),  # This should fallback
    ]

    portfolio = Portfolio(assets)

    print(f"Portfolio total value (INR): ₹{portfolio.total_value():,.2f}")
    print(f"Portfolio total invested (INR): ₹{portfolio.total_invested():,.2f}")

    # Test individual conversions
    usd_asset = assets[0]
    inr_value = converter.convert_to_inr(usd_asset.current_value, usd_asset.currency)
    print(f"USD asset value in INR: ₹{inr_value:,.2f}")

    # Test supported currencies
    currencies = converter.get_supported_currencies()
    print(f"Supported currencies: {len(currencies)}")
    print(f"Sample currencies: {currencies[:5]}")

    print("Currency conversion test completed!")

if __name__ == "__main__":
    test_currency_conversion()