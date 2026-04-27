import yfinance as yf
import pandas as pd


class MarketContext:

    def fetch_market_data(self):

        tickers = {
            "SP500": "^GSPC",
            "VIX": "^VIX",
            "GOLD": "GC=F",
            "BOND_YIELD": "^TNX"
        }

        series_list = []

        for name, symbol in tickers.items():

            df = yf.download(symbol, period="6mo", progress=False)

            if df.empty:
                print(f"Warning: No data for {symbol}")
                continue

            series = df["Close"]
            series.name = name

            series_list.append(series)

        if not series_list:
            raise ValueError("No market data retrieved")

        market_df = pd.concat(series_list, axis=1)

        return market_df


    def detect_regime(self, market_df):

        regime = "Unknown"
        vix_value = None
        trend = 0

        # VIX analysis
        if "VIX" in market_df.columns:

            vix_value = market_df["VIX"].iloc[-1]

            if vix_value > 25:
                regime = "High Volatility"

        # SP500 trend analysis
        if "SP500" in market_df.columns:

            sp500_returns = market_df["SP500"].pct_change().dropna()

            if not sp500_returns.empty:

                trend = sp500_returns.tail(30).mean()

                if regime != "High Volatility":

                    if trend > 0.002:
                        regime = "Bull Market"

                    elif trend < -0.002:
                        regime = "Bear Market"

                    else:
                        regime = "Sideways Market"

        return {
            "market_regime": regime,
            "vix": round(float(vix_value), 2) if vix_value else None,
            "sp500_trend": round(float(trend * 100), 2)
        }