import numpy as np


def portfolio_volatility(weights, cov_matrix):
    """
    Calculate annualized portfolio volatility
    """

    weights = np.array(weights)

    # Defensive check
    if len(weights) != cov_matrix.shape[0]:
        raise ValueError(
            f"Mismatch: weights={len(weights)} vs assets={cov_matrix.shape[0]}"
        )

    volatility = np.sqrt(weights.T @ cov_matrix @ weights)

    return volatility * np.sqrt(252)


def diversification_score(portfolio):
    
    asset_types = set(asset.asset_type for asset in portfolio.assets)
    num_assets = len(portfolio.assets)

    score = min(100, (len(asset_types) * 15) + (num_assets * 5))

    return score