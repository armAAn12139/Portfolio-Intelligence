from models.assets import Asset
from models.portfolio import Portfolio
from portfolio.portfolio_analyzer import PortfolioAnalyzer
from utils.helpers import print_portfolio_report


portfolio = Portfolio(
    assets=[
        Asset("BTC-USD","crypto",100000,120000),
        Asset("ETH-USD","crypto",90000,110000),
        Asset("TSLA","stock",80000,100000),
        Asset("NVDA","stock",70000,90000),
        Asset("CASH","cash",5000,5000)
    ]
)

analyzer = PortfolioAnalyzer(portfolio)

result = analyzer.analyze()

print_portfolio_report(result)