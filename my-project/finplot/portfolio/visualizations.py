"""
Advanced portfolio visualization functions using Plotly
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_performance_timeline(price_data: pd.DataFrame, portfolio_assets: list) -> go.Figure:
    """
    Create a line chart showing portfolio value growth over time.
    
    Args:
        price_data: DataFrame with price history (index=dates, columns=symbols)
        portfolio_assets: List of Asset objects in portfolio
        
    Returns:
        Plotly Figure object
    """
    # Calculate portfolio value over time based on asset prices
    portfolio_values = pd.Series(0.0, index=price_data.index)
    
    for asset in portfolio_assets:
        if asset.symbol in price_data.columns:
            # Calculate value trajectory for this asset
            price_history = price_data[asset.symbol]
            # Initial investment is asset.amount_invested, current value is asset.current_value
            # Calculate the percentage change from first to last price
            if price_history.iloc[0] > 0:
                pct_change = price_history / price_history.iloc[0]
                asset_value_history = asset.amount_invested * pct_change
                portfolio_values += asset_value_history
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=portfolio_values.index,
        y=portfolio_values.values,
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#1f77b4', width=3),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.2)'
    ))
    
    fig.update_layout(
        title='Portfolio Performance Over Time',
        xaxis_title='Date',
        yaxis_title='Portfolio Value (₹)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def create_asset_performance_heatmap(price_data: pd.DataFrame, portfolio_assets: list) -> go.Figure:
    """
    Create a heatmap showing asset performance metrics.
    Displays return percentage for each asset.
    
    Args:
        price_data: DataFrame with price history
        portfolio_assets: List of Asset objects
        
    Returns:
        Plotly Figure object
    """
    performance_data = []
    
    for asset in portfolio_assets:
        if asset.symbol in price_data.columns:
            prices = price_data[asset.symbol]
            price_return = ((prices.iloc[-1] / prices.iloc[0] - 1) * 100) if prices.iloc[0] > 0 else 0
            volatility = prices.pct_change().std() * np.sqrt(252) * 100  # Annualized
            max_price = prices.max()
            min_price = prices.min()
            
            performance_data.append({
                'Asset': asset.symbol,
                'Return (%)': price_return,
                'Volatility (%)': volatility,
                'Max Price': max_price,
                'Min Price': min_price
            })
    
    if not performance_data:
        return go.Figure().add_annotation(text="No performance data available")
    
    perf_df = pd.DataFrame(performance_data)
    
    # Create heatmap data: assets vs metrics
    metrics = ['Return (%)', 'Volatility (%)']
    heatmap_data = []
    
    for metric in metrics:
        heatmap_data.append(perf_df[metric].values)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=perf_df['Asset'].values,
        y=metrics,
        colorscale='RdYlGn',
        zmid=0,
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Asset Performance Heatmap',
        xaxis_title='Asset',
        yaxis_title='Metric',
        height=300,
        template='plotly_white'
    )
    
    return fig


def create_risk_return_scatter(price_data: pd.DataFrame, portfolio_assets: list, weights: list) -> go.Figure:
    """
    Create a scatter plot showing Risk vs Return for each asset.
    Bubble size represents allocation weight.
    
    Args:
        price_data: DataFrame with price history
        portfolio_assets: List of Asset objects
        weights: Portfolio weights for each asset
        
    Returns:
        Plotly Figure object
    """
    scatter_data = []
    
    for asset, weight in zip(portfolio_assets, weights):
        if asset.symbol in price_data.columns:
            prices = price_data[asset.symbol]
            returns = prices.pct_change().dropna()
            
            annual_return = ((prices.iloc[-1] / prices.iloc[0] - 1) * 100) if prices.iloc[0] > 0 else 0
            annual_volatility = returns.std() * np.sqrt(252) * 100
            
            scatter_data.append({
                'Asset': asset.symbol,
                'Return': annual_return,
                'Risk': annual_volatility,
                'Weight': weight * 100
            })
    
    if not scatter_data:
        return go.Figure().add_annotation(text="No scatter data available")
    
    scatter_df = pd.DataFrame(scatter_data)
    
    fig = px.scatter(
        scatter_df,
        x='Risk',
        y='Return',
        size='Weight',
        hover_data='Asset',
        title='Risk vs Return Analysis',
        labels={'Risk': 'Volatility (% annualized)', 'Return': 'Return (%)'},
        color='Return',
        color_continuous_scale='RdYlGn',
        height=400
    )
    
    fig.update_layout(
        hovermode='closest',
        template='plotly_white'
    )
    
    return fig


def create_cumulative_returns_chart(price_data: pd.DataFrame, portfolio_assets: list) -> go.Figure:
    """
    Create a line chart showing cumulative returns for each asset.
    
    Args:
        price_data: DataFrame with price history
        portfolio_assets: List of Asset objects
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    for asset in portfolio_assets:
        if asset.symbol in price_data.columns:
            prices = price_data[asset.symbol]
            cumulative_return = (prices / prices.iloc[0] - 1) * 100
            
            fig.add_trace(go.Scatter(
                x=cumulative_return.index,
                y=cumulative_return.values,
                mode='lines',
                name=asset.symbol,
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Return: %{y:.2f}%<extra></extra>'
            ))
    
    fig.update_layout(
        title='Cumulative Returns by Asset',
        xaxis_title='Date',
        yaxis_title='Cumulative Return (%)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def create_drawdown_chart(price_data: pd.DataFrame, portfolio_assets: list) -> go.Figure:
    """
    Create a drawdown chart showing peak-to-trough declines for portfolio.
    
    Args:
        price_data: DataFrame with price history
        portfolio_assets: List of Asset objects
        
    Returns:
        Plotly Figure object
    """
    # Calculate portfolio value over time
    portfolio_values = pd.Series(0.0, index=price_data.index)
    
    for asset in portfolio_assets:
        if asset.symbol in price_data.columns:
            price_history = price_data[asset.symbol]
            if price_history.iloc[0] > 0:
                pct_change = price_history / price_history.iloc[0]
                asset_value_history = asset.amount_invested * pct_change
                portfolio_values += asset_value_history
    
    # Calculate running maximum
    running_max = portfolio_values.expanding().max()
    
    # Calculate drawdown as percentage from peak
    drawdown = (portfolio_values - running_max) / running_max * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=drawdown.index,
        y=drawdown.values,
        mode='lines',
        name='Drawdown',
        line=dict(color='#d62728', width=2),
        fill='tozeroy',
        fillcolor='rgba(214, 39, 40, 0.3)'
    ))
    
    # Add 0 reference line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="No Drawdown")
    
    fig.update_layout(
        title='Portfolio Drawdown Over Time',
        xaxis_title='Date',
        yaxis_title='Drawdown (%)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def create_correlation_heatmap(returns_data: pd.DataFrame) -> go.Figure:
    """
    Create a correlation matrix heatmap showing asset relationships.
    
    Args:
        returns_data: DataFrame with daily returns (symbols as columns)
        
    Returns:
        Plotly Figure object
    """
    correlation = returns_data.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation.values,
        x=correlation.columns,
        y=correlation.index,
        colorscale='RdBu',
        zmid=0,
        zmin=-1,
        zmax=1,
        text=correlation.values,
        texttemplate='%{text:.2f}',
        hovertemplate='<b>%{x} vs %{y}</b><br>Correlation: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Asset Correlation Matrix',
        xaxis_title='Asset',
        yaxis_title='Asset',
        height=500,
        template='plotly_white'
    )
    
    return fig


def create_portfolio_treemap(allocation: dict) -> go.Figure:
    """
    Create a treemap showing hierarchical portfolio composition.
    
    Args:
        allocation: Dictionary with asset symbols as keys and percentages as values
        
    Returns:
        Plotly Figure object
    """
    # Prepare data for treemap
    labels = ['Portfolio'] + list(allocation.keys())
    parents = [''] + ['Portfolio'] * len(allocation)
    values = [sum(allocation.values())] + list(allocation.values())
    
    # Create hover text with percentages
    hover_text = ['Portfolio']
    for asset, pct in allocation.items():
        hover_text.append(f'{asset}<br>{pct:.1f}%')
    
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        hovertext=hover_text,
        hoverinfo='label+value',
        textposition='middle center',
        marker=dict(colorscale='Viridis'),
        textfont=dict(size=12)
    ))
    
    fig.update_layout(
        title='Portfolio Composition Treemap',
        height=500,
        template='plotly_white'
    )
    
    return fig
