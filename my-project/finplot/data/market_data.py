import yfinance as yf
import pandas as pd
from utils.live_market import translate_to_yf_symbol


def fetch_price_history(symbol: str, period: str = "1y"):
    """
    Fetch historical closing prices for a single asset
    """

    try:
        # Convert symbol to Yahoo Finance format (e.g., BIOCON -> BIOCON.NS)
        yf_symbol = translate_to_yf_symbol(symbol)
        data = yf.download(yf_symbol, period=period, progress=False)

        if data.empty:
            print(f"Warning: No market data found for {symbol}")
            return None

        prices = data["Close"]

        prices.name = symbol

        return prices

    except Exception as e:

        print(f"Error fetching {symbol}: {e}")

        return None


def fetch_multiple_assets(symbols, period: str = "1y"):
    """
    Fetch historical price data for multiple assets and combine into one DataFrame
    """

    price_series = []

    for symbol in symbols:

        series = fetch_price_history(symbol, period)

        if series is None:
            continue

        price_series.append(series)

    if not price_series:
        raise ValueError("No valid market data retrieved")

    # Combine into a single dataframe
    price_df = pd.concat(price_series, axis=1)

    # Ensure dates align
    price_df = price_df.dropna()

    return price_df