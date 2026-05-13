from models.assets import Asset
from models.portfolio import Portfolio
from portfolio.portfolio_analyzer import PortfolioAnalyzer
from utils.helpers import print_portfolio_report


portfolio = Portfolio(
    assets=[
        Asset("BTC-USD","crypto",100000,120000, "INR"),  # Values in INR
        Asset("ETH-USD","crypto",90000,110000, "INR"),   # Values in INR
        Asset("TSLA","stock",80000,100000, "INR"),       # Values in INR
        Asset("NVDA","stock",70000,90000, "INR"),        # Values in INR
        Asset("CASH","cash",5000,5000, "INR")            # Values in INR
    ]
)

analyzer = PortfolioAnalyzer(portfolio)

result = analyzer.analyze()

print_portfolio_report(result)