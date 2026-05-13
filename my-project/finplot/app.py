import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from models.assets import Asset
from models.portfolio import Portfolio
from portfolio.portfolio_analyzer import PortfolioAnalyzer
from utils.currency_converter import converter
from utils.live_market import fetch_live_prices, fetch_current_price, get_default_watchlist
from utils.symbols import ALL_SYMBOLS, get_symbols_by_category, format_symbol_option

st.set_page_config(page_title="FinPlot - Portfolio Intelligence", page_icon="📈", layout="wide")

st.title("📈 FinPlot - Portfolio Intelligence")
st.markdown("### *Your Smart Portfolio Companion* 💡")

st.sidebar.header("🎯 Portfolio Setup")

# Currency selection info
st.sidebar.markdown("---")
st.sidebar.subheader("💱 Currency Support")
st.sidebar.markdown("All values will be converted to INR for analysis")
supported_currencies = converter.get_supported_currencies()
st.sidebar.markdown(f"Supported currencies: {', '.join(supported_currencies[:5])}...")

# Live market snapshot settings
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Live Market Feed")
auto_refresh = st.sidebar.checkbox("Auto-refresh live prices", value=True)
refresh_interval = st.sidebar.slider("Refresh interval (seconds)", min_value=15, max_value=180, value=60, step=15)
if auto_refresh:
    components.html(f"<script>setTimeout(()=>window.location.reload(), {refresh_interval * 1000});</script>", height=0)

symbol_options = sorted(ALL_SYMBOLS.keys())
symbol_display_options = [format_symbol_option(s) for s in symbol_options]

with st.sidebar.expander("🔎 Live Lookup", expanded=True):
    selected_live = st.selectbox("Search symbol for live price", symbol_display_options, key="live_lookup", help="Search and display live market price for any major stock or crypto")
    selected_live_symbol = selected_live.split(" - ")[0] if selected_live else ""
    if selected_live_symbol:
        live_info = fetch_current_price(selected_live_symbol)
        price_text = f"{live_info['price']:,}" if live_info['price'] is not None else "N/A"
        change_text = f"{live_info['change_pct']:+.2f}%" if live_info['change_pct'] is not None else "N/A"
        st.metric(f"{selected_live_symbol} live price", price_text, delta=change_text)

    st.markdown("---")
    st.write("**Gold price**")
    gold_info = fetch_current_price("GOLD")
    gold_price = f"{gold_info['price']:,}" if gold_info['price'] is not None else "N/A"
    gold_change = f"{gold_info['change_pct']:+.2f}%" if gold_info['change_pct'] is not None else "N/A"
    st.metric("GOLD", gold_price, delta=gold_change)

    st.markdown("---")
    if st.button("Refresh exchange rates"):
        converter.refresh_rates()
    rates = converter.get_rates()
    rate_rows = [f"{cur}: {rate:.4f}" for cur, rate in list(rates.items())[:10]]
    st.write("**Currency Rates (INR base)**")
    for row in rate_rows:
        st.caption(row)

    st.markdown("---")
    st.write("**Quick Watchlist**")
    watchlist_symbols = get_default_watchlist()
    watchlist_df = fetch_live_prices(watchlist_symbols)
    st.dataframe(watchlist_df, use_container_width=True, hide_index=True)

# Symbol reference section
st.sidebar.markdown("---")
with st.sidebar.expander("📋 Available Symbols Reference"):
    symbols_by_category = get_symbols_by_category()
    for category, symbols in symbols_by_category.items():
        st.markdown(f"**{category}**")
        # Show first 10 symbols per category
        displayed_symbols = sorted(symbols.keys())[:10]
        symbols_text = ", ".join(displayed_symbols)
        if len(symbols) > 10:
            st.caption(f"{symbols_text}... (+{len(symbols)-10} more)")
        else:
            st.caption(symbols_text)
        st.markdown("")

# Input for assets
num_assets = st.sidebar.number_input("Number of Assets", min_value=1, value=5, help="How many investments do you have?")

assets = []
for i in range(num_assets):
    with st.sidebar.expander(f"📊 Asset {i+1}"):
        # Symbol selection with search
        st.markdown(f"**Select Symbol {i+1}**")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Create symbol options
            symbol_options = sorted(ALL_SYMBOLS.keys())
            symbol_display_options = [f"{s} - {ALL_SYMBOLS[s]}" for s in symbol_options]
            
            selected_option = st.selectbox(
                f"Search for symbol {i+1}",
                symbol_display_options,
                key=f"symbol_{i}",
                help="Search and select from major Indian stocks, cryptocurrencies, and indices"
            )
            # Extract just the symbol from the selected option
            symbol = selected_option.split(" - ")[0] if selected_option else ""
        
        with col2:
            st.markdown("**Or Enter Custom**")
            custom_symbol = st.text_input(f"Custom {i+1}", key=f"custom_symbol_{i}", placeholder="e.g., AAPL", label_visibility="collapsed")
            if custom_symbol:
                symbol = custom_symbol
        
        asset_type = st.selectbox(f"Type {i+1}", ["stock", "crypto", "bond", "cash"], key=f"type_{i}")
        currency = st.selectbox(f"Currency {i+1}", supported_currencies, index=supported_currencies.index("INR") if "INR" in supported_currencies else 0, key=f"currency_{i}")
        current_value = st.number_input(f"Current Value {i+1}", min_value=0.0, key=f"value_{i}", help=f"Value in {currency}")
        purchase_price = st.number_input(f"Purchase Price {i+1}", min_value=0.0, key=f"purchase_{i}", help=f"Purchase price in {currency}")

        if symbol and current_value > 0:
            assets.append(Asset(symbol, asset_type, purchase_price, current_value, currency))

if st.sidebar.button("🚀 Analyze Portfolio", type="primary"):
    if assets:
        portfolio = Portfolio(assets)
        analyzer = PortfolioAnalyzer(portfolio)

        with st.spinner("🔍 Crunching numbers... Analyzing your portfolio magic! ✨"):
            result = analyzer.analyze()

        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Analysis", "🎲 What-If", "💡 Insights"])

        with tab1:
            st.header("Portfolio Overview")
            
            # Key metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💰 Total Value", f"₹{result['portfolio_value']:,.0f}", delta=f"{result['return_rate']:+.1f}%")
            with col2:
                st.metric("📊 Volatility", f"{result['volatility']}%")
            with col3:
                st.metric("🎯 Risk Score", f"{result['risk_score']}/100", help=f"Level: {result['risk_level']}")
            with col4:
                st.metric("🌟 Diversification", f"{result['diversification_score']}/100")

            # Risk gauge
            st.subheader("Risk Meter")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['risk_score'],
                title={'text': "Portfolio Risk"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': "darkblue"},
                       'steps': [
                           {'range': [0, 20], 'color': "lightgreen"},
                           {'range': [20, 40], 'color': "yellow"},
                           {'range': [40, 60], 'color': "orange"},
                           {'range': [60, 100], 'color': "red"}]}))
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.header("Detailed Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Asset Allocation")
                allocation_df = pd.DataFrame.from_dict(result['allocation'], orient='index', columns=['Percentage'])
                fig = px.pie(allocation_df, values='Percentage', names=allocation_df.index, 
                           title="Portfolio Allocation", hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Sector Exposure")
                sector_df = pd.DataFrame.from_dict(result['sector_exposure'], orient='index', columns=['Percentage'])
                fig = px.bar(sector_df, x=sector_df.index, y='Percentage', 
                           title="Sector Breakdown", color='Percentage')
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("Optimal Allocation")
            optimal_df = pd.DataFrame.from_dict(result['optimal_allocation'], orient='index', columns=['Weight'])
            optimal_df = optimal_df[optimal_df['Weight'] > 0.01]  # Filter small weights
            optimal_df['Weight'] = optimal_df['Weight'] * 100  # Convert to percentage
            fig = px.bar(optimal_df, x=optimal_df.index, y='Weight', 
                       title="Suggested Optimal Weights", color='Weight')
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.header("What-If Scenarios 🎲")
            st.markdown("Adjust allocations and see how it affects your portfolio!")

            # Simple what-if: adjust one asset's weight
            st.subheader("Adjust Asset Weight")
            asset_options = list(result['allocation'].keys())
            selected_asset = st.selectbox("Select Asset to Adjust", asset_options)
            current_weight = result['allocation'][selected_asset]
            new_weight = st.slider(f"New weight for {selected_asset}", 0.0, 100.0, float(current_weight), 1.0)

            if st.button("Recalculate"):
                try:
                    # Create adjusted allocation
                    adjusted_allocation = result['allocation'].copy()
                    adjusted_allocation[selected_asset] = new_weight
                    
                    # Calculate remaining percentage for other assets
                    total_other = 100.0 - new_weight
                    
                    # Get other assets
                    other_assets = [k for k in adjusted_allocation.keys() if k != selected_asset]
                    
                    if other_assets and total_other > 0:
                        # Calculate current total of other assets
                        current_other_total = sum(adjusted_allocation[a] for a in other_assets)
                        
                        if current_other_total > 0:
                            # Scale other assets proportionally to fill remaining space
                            scale_factor = total_other / current_other_total
                            for asset in other_assets:
                                adjusted_allocation[asset] = adjusted_allocation[asset] * scale_factor
                        else:
                            # If no other assets have allocation, distribute equally
                            equal_share = total_other / len(other_assets)
                            for asset in other_assets:
                                adjusted_allocation[asset] = equal_share
                    elif total_other == 0:
                        # Set other assets to 0
                        for asset in other_assets:
                            adjusted_allocation[asset] = 0.0
                    else:
                        # If negative, this is invalid
                        st.error("❌ Invalid allocation: Total exceeds 100%")
                        adjusted_allocation = result['allocation'].copy()  # Reset
                    
                    # Ensure total is exactly 100% (rounding fix)
                    total_check = sum(adjusted_allocation.values())
                    if abs(total_check - 100.0) > 0.01:
                        # Adjust the selected asset to make total exactly 100%
                        adjusted_allocation[selected_asset] += (100.0 - total_check)
                    
                    st.subheader("Adjusted Allocation")
                    adj_df = pd.DataFrame.from_dict(adjusted_allocation, orient='index', columns=['Percentage'])
                    fig = px.pie(adj_df, values='Percentage', names=adj_df.index, title="What-If Allocation")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show summary
                    st.write(f"**{selected_asset}**: {adjusted_allocation[selected_asset]:.1f}%")
                    if other_assets:
                        st.write(f"**Other assets**: {total_other:.1f}% total")
                    
                except Exception as e:
                    st.error(f"❌ Error in recalculation: {str(e)}")
                    st.info("💡 Try adjusting the weight to a valid percentage (0-100%)")

        with tab4:
            st.header("AI Insights & Recommendations")
            
            st.subheader("💡 Key Insights")
            for insight in result['insights']:
                st.info(f"• {insight}")

            st.subheader("🎯 Recommendations")
            for rec in result['recommendations']:
                st.success(f"• {rec}")

            # Market context
            st.subheader("🌍 Market Context")
            market = result['market_context']
            st.write(f"**Market Regime:** {market.get('market_regime', 'Unknown')}")
            st.write(f"**VIX Level:** {market.get('vix', 'N/A')}")

    else:
        st.error("❌ Please enter at least one asset with a symbol and current value!")

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by FinPlot Team")
st.sidebar.markdown("[📖 Documentation](https://github.com/your-repo) | [🐛 Report Issues](https://github.com/your-repo/issues)")