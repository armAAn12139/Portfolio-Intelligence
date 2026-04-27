import numpy as np
from scipy.optimize import minimize


class PortfolioOptimizer:

    def __init__(self, risk_free_rate=0.02):
        self.risk_free_rate = risk_free_rate

    # ---------- Core Metrics ----------

    def portfolio_performance(self, weights, mean_returns, cov_matrix):
        returns = np.dot(weights, mean_returns)
        volatility = np.sqrt(weights.T @ cov_matrix @ weights)
        return returns, volatility

    # ---------- Min Variance ----------

    def minimize_volatility(self, weights, mean_returns, cov_matrix):
        return self.portfolio_performance(weights, mean_returns, cov_matrix)[1]

    def get_min_variance_portfolio(self, mean_returns, cov_matrix):
        num_assets = len(mean_returns)

        init_weights = np.ones(num_assets) / num_assets
        bounds = tuple((0, 1) for _ in range(num_assets))
        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]

        result = minimize(
            self.minimize_volatility,
            init_weights,
            args=(mean_returns, cov_matrix),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        return result.x

    # ---------- Max Sharpe ----------

    def negative_sharpe(self, weights, mean_returns, cov_matrix):
        ret, vol = self.portfolio_performance(weights, mean_returns, cov_matrix)
        return -(ret - self.risk_free_rate) / vol

    def get_max_sharpe_portfolio(self, mean_returns, cov_matrix):
        num_assets = len(mean_returns)

        init_weights = np.ones(num_assets) / num_assets
        bounds = tuple((0, 1) for _ in range(num_assets))
        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]

        result = minimize(
            self.negative_sharpe,
            init_weights,
            args=(mean_returns, cov_matrix),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        return result.x

    # ---------- Efficient Frontier ----------

    def efficient_frontier(self, mean_returns, cov_matrix, points=50):
        num_assets = len(mean_returns)

        bounds = tuple((0, 1) for _ in range(num_assets))
        base_constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]

        frontier = []

        target_returns = np.linspace(
            mean_returns.min(), mean_returns.max(), points
        )

        for target in target_returns:

            constraints = base_constraints + [
                {"type": "eq", "fun": lambda w, t=target: np.dot(w, mean_returns) - t}
            ]

            result = minimize(
                self.minimize_volatility,
                np.ones(num_assets) / num_assets,
                args=(mean_returns, cov_matrix),
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
            )

            if result.success:
                ret, vol = self.portfolio_performance(
                    result.x, mean_returns, cov_matrix
                )

                frontier.append({
                    "return": float(ret),
                    "volatility": float(vol),
                    "weights": result.x.tolist()
                })

        return frontier

    # ---------- Public API ----------

    def optimize(self, returns_df):

        returns_df = returns_df.dropna(axis=1)  # enforce clean assets

        mean_returns = returns_df.mean().values
        cov_matrix = returns_df.cov().values
        assets = returns_df.columns.tolist()

        num_assets = len(mean_returns)

        init_weights = np.ones(num_assets) / num_assets

        bounds = tuple((0, 1) for _ in range(num_assets))
        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]

        def portfolio_volatility(weights):
            return np.sqrt(weights.T @ cov_matrix @ weights)

        result = minimize(
            portfolio_volatility,
            init_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        weights = result.x

        return {
            "weights": weights,
            "assets": assets,
            "cov_matrix": cov_matrix,
        }