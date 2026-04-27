def print_portfolio_report(result):

    print("\n------ Portfolio Intelligence Report ------\n")

    print(f"Total Portfolio Value: ₹{result['portfolio_value']}")

    # Asset Allocation
    print("\nAsset Allocation:")
    for asset, pct in result["allocation"].items():
        print(f"{asset}: {pct}%")

    # Sector Exposure
    if "sector_exposure" in result:
        print("\nSector Exposure:")
        for sector, pct in result["sector_exposure"].items():
            print(f"{sector}: {pct}%")

    # Risk metrics
    print(f"\nPortfolio Volatility: {result['volatility']}%")
    print(f"Portfolio Return: {result['return_rate']}%")
    print(f"Risk Score: {result['risk_score']} / 100")
    print(f"Risk Level: {result['risk_level']}")

    print(f"Diversification Score: {result['diversification_score']}/100")

    # Market Context
    market = result["market_context"]

    print("\nMarket Context:")
    print(f"Market Regime: {market.get('market_regime')}")
    print(f"VIX: {market.get('vix')}")

    # Insights
    print("\nAI Insights:")
    for insight in result["insights"]:
        print(f"- {insight}")

    #optimization
    print("\nOptimal Portfolio Allocation:")
    for asset, pct in result["optimal_allocation"].items():
        if pct > 0.01:
            print(f"{asset}: {pct}%")



    # Recommendations
    print("\nInvestment Recommendations:")
    for rec in result["recommendations"]:
        print(f"- {rec}")



    print("\n------------------------------------------\n")