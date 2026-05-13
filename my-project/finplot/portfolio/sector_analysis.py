SECTOR_MAP = {
    "AAPL": "Technology",
    "MSFT": "Technology",
    "NVDA": "Technology",
    "TSLA": "Automotive",
    "GOOGL": "Technology",
    "AMZN": "Consumer",
    "META": "Technology",
    "JPM": "Financial",
    "BAC": "Financial",
    "KO": "Consumer Defensive",
    "PEP": "Consumer Defensive",
    "GLD": "Commodities",
    "TLT": "Bonds",
    "BTC-USD": "Crypto",
    "ETH-USD": "Crypto"
}


def calculate_sector_exposure(portfolio):
    from utils.currency_converter import converter

    total_value = portfolio.total_value()

    sector_weights = {}

    for asset in portfolio.assets:
        value_in_inr = converter.convert_to_inr(asset.current_value, asset.currency)
        sector = SECTOR_MAP.get(asset.symbol, "Other")

        weight = value_in_inr / total_value * 100

        sector_weights[sector] = sector_weights.get(sector, 0) + weight

    # round results
    for sector in sector_weights:
        sector_weights[sector] = round(sector_weights[sector], 2)

    return sector_weights