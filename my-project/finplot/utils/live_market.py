import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional
from utils.currency_converter import converter
from utils.symbols import ALL_SYMBOLS, INDIAN_STOCKS, SPECIAL_SYMBOLS, format_symbol_option

SYMBOL_OVERRIDES = {
    "GOLD": "GC=F",
    "SILVER": "SI=F",
    "NIFTY50": "^NSEI",
    "SENSEX": "^BSESN",
    "NIFTYIT": "^CNXIT",
    "NIFTYBANK": "^NSEBANK",
}

DEFAULT_STOCK_WATCHLIST = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "HINDUNILVR", "ITC", "AXISBANK", "SUNPHARMA", "LT"
]

DEFAULT_CRYPTO_WATCHLIST = [
    "BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "DOT-USD", "MATIC-USD", "LINK-USD"
]

def translate_to_yf_symbol(symbol: str) -> str:
    """Translate a user-friendly symbol to a yfinance ticker."""
    if symbol in SYMBOL_OVERRIDES:
        return SYMBOL_OVERRIDES[symbol]

    if symbol in INDIAN_STOCKS:
        return f"{symbol}.NS"

    return symbol


def fetch_current_price(symbol: str) -> Dict[str, Optional[float]]:
    """Fetch the latest price and intraday change for a symbol."""
    yf_symbol = translate_to_yf_symbol(symbol)
    result = {
        "symbol": symbol,
        "yf_symbol": yf_symbol,
        "name": ALL_SYMBOLS.get(symbol, symbol),
        "price": None,
        "change_pct": None,
        "currency": None,
    }

    try:
        ticker = yf.Ticker(yf_symbol)

        info = {}
        try:
            info = ticker.info or {}
        except Exception:
            info = {}

        price = None
        prev_close = None
        currency = info.get("currency")

        if info.get("regularMarketPrice") is not None:
            price = info.get("regularMarketPrice")
            prev_close = info.get("previousClose")
        elif info.get("currentPrice") is not None:
            price = info.get("currentPrice")
            prev_close = info.get("previousClose")

        if price is None:
            history = ticker.history(period="1d", interval="1m", progress=False)
            if not history.empty:
                price = float(history["Close"].iloc[-1])
                if len(history) > 1:
                    prev_close = float(history["Close"].iloc[-2])

        if price is not None:
            if symbol == "GOLD" or symbol == "SILVER":
                # Convert futures price from USD/oz to INR per 10g
                price_in_inr = converter.convert_to_inr(float(price), "USD")
                price_per_10g = price_in_inr / 31.1034768 * 10
                result["price"] = round(price_per_10g, 2)
                result["currency"] = "INR/10g"
            else:
                result["price"] = round(float(price), 2)
                result["currency"] = currency or ("INR" if symbol in INDIAN_STOCKS else currency)
            if prev_close is not None and prev_close != 0:
                result["change_pct"] = round((float(price) - float(prev_close)) / float(prev_close) * 100, 2)

    except Exception:
        pass

    return result


def fetch_live_prices(symbols: List[str]) -> pd.DataFrame:
    """Fetch the latest live prices for a list of symbols."""
    rows = []
    for symbol in symbols:
        row = fetch_current_price(symbol)
        rows.append({
            "Symbol": row["symbol"],
            "Name": row["name"],
            "Price": row["price"],
            "Change (%)": row["change_pct"],
            "Currency": row["currency"] or "N/A",
        })

    df = pd.DataFrame(rows)
    return df


def get_default_watchlist() -> List[str]:
    """Return a default subset of symbols for quick live market snapshot."""
    return DEFAULT_STOCK_WATCHLIST + DEFAULT_CRYPTO_WATCHLIST + ["GOLD"]
