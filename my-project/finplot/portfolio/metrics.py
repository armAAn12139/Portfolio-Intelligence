import numpy as np
import pandas as pd
from utils.currency_converter import converter


def calculate_allocation(portfolio):
    """
    Calculate asset allocation percentages
    """
    total_value = portfolio.total_value()

    allocation = {}

    for asset in portfolio.assets:
        value_in_inr = converter.convert_to_inr(asset.current_value, asset.currency)
        allocation[asset.symbol] = round(
            (value_in_inr / total_value) * 100, 2
        )

    return allocation


def calculate_returns(price_df: pd.DataFrame):
    """
    Convert price data into daily returns
    """
    return price_df.pct_change().dropna()


def correlation_matrix(returns_df):
    """
    Asset correlation matrix
    """
    return returns_df.corr()


def portfolio_volatility(weights, cov_matrix):
    """
    Calculate portfolio volatility (standard deviation)
    """
    return np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))


def diversification_score(portfolio):
    """
    Calculate diversification score based on asset types and number of assets
    """
    asset_types = set(asset.asset_type for asset in portfolio.assets)
    num_assets = len(portfolio.assets)

    score = min(100, (len(asset_types) * 15) + (num_assets * 5))

    return score