#!/usr/bin/env python
"""
Test script to validate the improved risk calculator
"""

from models.portfolio import Portfolio
from models.assets import Asset
from portfolio.portfolio_analyzer import PortfolioAnalyzer

print("=" * 60)
print("RISK CALCULATOR TEST")
print("=" * 60)

# Test Case 1: Well-diversified, low-risk portfolio
print("\n[TEST 1] Low-Risk, Well-Diversified Portfolio")
print("-" * 60)
portfolio1 = Portfolio(assets=[
    Asset("IVV", "stock", 50000, "USD"),      # S&P 500
    Asset("VTV", "stock", 30000, "USD"),      # Value stocks
    Asset("BND", "bond", 20000, "USD"),       # Bonds
    Asset("GLD", "etf", 10000, "USD"),        # Gold
])

try:
    analyzer1 = PortfolioAnalyzer(portfolio1)
    result1 = analyzer1.analyze()
    print(f"Portfolio Value: ₹{result1['portfolio_value']:,.0f}")
    print(f"Risk Score: {result1['risk_score']}/100")
    print(f"Risk Level: {result1['risk_level']}")
    print(f"Volatility: {result1['volatility']}%")
    print(f"Diversification: {result1['diversification_score']}/100")
    print(f"Return Rate: {result1['return_rate']}%")
    print("✓ Expected: Low risk score (10-25)")
except Exception as e:
    print(f"✗ Error: {e}")

# Test Case 2: Highly concentrated, high-risk portfolio
print("\n[TEST 2] High-Risk, Concentrated Portfolio")
print("-" * 60)
portfolio2 = Portfolio(assets=[
    Asset("NVDA", "stock", 70000, "USD"),     # 70% in single tech stock
    Asset("TSLA", "stock", 30000, "USD"),     # 30% in another tech stock
])

try:
    analyzer2 = PortfolioAnalyzer(portfolio2)
    result2 = analyzer2.analyze()
    print(f"Portfolio Value: ₹{result2['portfolio_value']:,.0f}")
    print(f"Risk Score: {result2['risk_score']}/100")
    print(f"Risk Level: {result2['risk_level']}")
    print(f"Volatility: {result2['volatility']}%")
    print(f"Diversification: {result2['diversification_score']}/100")
    print(f"Return Rate: {result2['return_rate']}%")
    print("✓ Expected: High risk score (60-90)")
except Exception as e:
    print(f"✗ Error: {e}")

# Test Case 3: Moderate portfolio with some crypto
print("\n[TEST 3] Moderate Portfolio with Crypto")
print("-" * 60)
portfolio3 = Portfolio(assets=[
    Asset("SPY", "stock", 40000, "USD"),      # 40% stocks
    Asset("QQQ", "stock", 25000, "USD"),      # 25% tech
    Asset("BTC", "crypto", 20000, "USD"),     # 20% crypto
    Asset("AGG", "bond", 15000, "USD"),       # 15% bonds
])

try:
    analyzer3 = PortfolioAnalyzer(portfolio3)
    result3 = analyzer3.analyze()
    print(f"Portfolio Value: ₹{result3['portfolio_value']:,.0f}")
    print(f"Risk Score: {result3['risk_score']}/100")
    print(f"Risk Level: {result3['risk_level']}")
    print(f"Volatility: {result3['volatility']}%")
    print(f"Diversification: {result3['diversification_score']}/100")
    print(f"Return Rate: {result3['return_rate']}%")
    print("✓ Expected: Moderate risk score (35-55)")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
print("\nSummary:")
print("- Low-risk portfolios should score 10-25")
print("- Moderate portfolios should score 35-55")
print("- High-risk portfolios should score 60-90")
print("- Risk scores should NOT be stuck at 0-5%")
