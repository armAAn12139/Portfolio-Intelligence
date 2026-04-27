import streamlit as st
import pandas as pd
from models.assets import Asset
from models.portfolio import Portfolio
from portfolio.portfolio_analyzer import PortfolioAnalyzer

st.title("FinPlot - Portfolio Intelligence")

st.sidebar.header("Portfolio Input")

# Input for assets
num_assets = st.sidebar.number_input("Number of Assets", min_value=1, value=5)

assets = []
for i in range(num_assets):
    st.sidebar.subheader(f"Asset {i+1}")
    symbol = st.sidebar.text_input(f"Symbol {i+1}", key=f"symbol_{i}")
    asset_type = st.sidebar.selectbox(f"Type {i+1}", ["stock", "crypto", "bond", "cash"], key=f"type_{i}")
    current_value = st.sidebar.number_input(f"Current Value {i+1}", min_value=0.0, key=f"value_{i}")
    purchase_price = st.sidebar.number_input(f"Purchase Price {i+1}", min_value=0.0, key=f"purchase_{i}")

    if symbol and current_value > 0:
        assets.append(Asset(symbol, asset_type, purchase_price, current_value))

if st.sidebar.button("Analyze Portfolio"):
    if assets:
        portfolio = Portfolio(assets)
        analyzer = PortfolioAnalyzer(portfolio)

        with st.spinner("Analyzing portfolio..."):
            result = analyzer.analyze()

        # Display results
        st.header("Portfolio Analysis Results")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Portfolio Value")
            st.metric("Total Value", f"₹{result['portfolio_value']:,.0f}")

            st.subheader("Risk Metrics")
            st.metric("Volatility", f"{result['volatility']}%")
            st.metric("Return", f"{result['return_rate']}%")
            st.metric("Risk Score", f"{result['risk_score']}/100")
            st.metric("Risk Level", result['risk_level'])
            st.metric("Diversification Score", f"{result['diversification_score']}/100")

        with col2:
            st.subheader("Asset Allocation")
            allocation_df = pd.DataFrame.from_dict(result['allocation'], orient='index', columns=['Percentage'])
            st.bar_chart(allocation_df)

            st.subheader("Sector Exposure")
            sector_df = pd.DataFrame.from_dict(result['sector_exposure'], orient='index', columns=['Percentage'])
            st.bar_chart(sector_df)

        st.subheader("Market Context")
        market = result['market_context']
        st.write(f"Market Regime: {market.get('market_regime', 'Unknown')}")
        st.write(f"VIX: {market.get('vix', 'N/A')}")

        st.subheader("AI Insights")
        for insight in result['insights']:
            st.write(f"• {insight}")

        st.subheader("Optimal Allocation")
        optimal_df = pd.DataFrame.from_dict(result['optimal_allocation'], orient='index', columns=['Weight'])
        optimal_df = optimal_df[optimal_df['Weight'] > 0.01]  # Filter small weights
        optimal_df['Weight'] = optimal_df['Weight'] * 100  # Convert to percentage
        st.bar_chart(optimal_df)

        st.subheader("Investment Recommendations")
        for rec in result['recommendations']:
            st.write(f"• {rec}")

    else:
        st.error("Please enter at least one asset.")

st.sidebar.markdown("---")
st.sidebar.markdown("Built with Streamlit & FinPlot")