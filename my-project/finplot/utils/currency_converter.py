import requests
from typing import Dict, Optional
import json

class CurrencyConverter:
    """
    Currency conversion utility using free API
    """

    def __init__(self):
        self.rates: Dict[str, float] = {}
        self.base_currency = "INR"  # Indian Rupee as base
        self._load_rates()

    def _load_rates(self):
        """
        Load exchange rates from API
        """
        try:
            # Using free API - you might want to use a paid service for production
            url = f"https://api.exchangerate-api.com/v4/latest/{self.base_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.rates = data.get("rates", {})
        except Exception as e:
            print(f"Warning: Could not load exchange rates: {e}")
            # Fallback rates (approximate as of 2024)
            self.rates = {
                "USD": 0.012,  # 1 INR = ~0.012 USD
                "EUR": 0.011,  # 1 INR = ~0.011 EUR
                "GBP": 0.0095, # 1 INR = ~0.0095 GBP
                "JPY": 1.75,   # 1 INR = ~1.75 JPY
                "INR": 1.0     # Base currency
            }

    def convert_to_inr(self, amount: float, from_currency: str) -> float:
        """
        Convert amount from given currency to INR
        """
        if from_currency == self.base_currency:
            return amount

        if from_currency not in self.rates:
            print(f"Warning: No exchange rate for {from_currency}, using as-is")
            return amount

        # Convert to INR: amount * (INR per unit of from_currency)
        return amount * (1 / self.rates[from_currency])

    def convert_from_inr(self, amount: float, to_currency: str) -> float:
        """
        Convert amount from INR to given currency
        """
        if to_currency == self.base_currency:
            return amount

        if to_currency not in self.rates:
            print(f"Warning: No exchange rate for {to_currency}, using as-is")
            return amount

        # Convert from INR: amount * (to_currency per INR)
        return amount * self.rates[to_currency]

    def get_supported_currencies(self) -> list:
        """
        Get list of supported currencies
        """
        return list(self.rates.keys())

# Global instance
converter = CurrencyConverter()