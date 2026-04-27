from data.market_data import fetch_multiple_assets
from portfolio.metrics import calculate_allocation, portfolio_volatility, diversification_score, calculate_returns
from portfolio.sector_analysis import calculate_sector_exposure
from market.market_context import MarketContext
from portfolio.optimizer import PortfolioOptimizer
from recommendation.recommendation_engine import RecommendationEngine


class PortfolioAnalyzer:

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.market_engine = MarketContext()
        self.optimizer = PortfolioOptimizer()
        self.recommendation_engine = RecommendationEngine()

    def analyze(self):

        # -----------------------------
        # Step 1: Define symbols
        # -----------------------------
        portfolio_symbols = [
            asset.symbol
            for asset in self.portfolio.assets
            if asset.symbol != "CASH"
        ]

        # Extended universe (for optimizer only)
        extended_symbols = portfolio_symbols + ["SPY", "GLD", "TLT"]

        # -----------------------------
        # Step 2: Fetch market data
        # -----------------------------
        price_data_full = fetch_multiple_assets(extended_symbols)

        # Filter to available symbols
        available_symbols = price_data_full.columns.tolist()
        portfolio_symbols = [s for s in portfolio_symbols if s in available_symbols]

        if not portfolio_symbols:
            raise ValueError("No market data available for portfolio assets")

        returns_full = calculate_returns(price_data_full)

        # -----------------------------
        # Step 3: Create portfolio-only returns (CRITICAL FIX)
        # -----------------------------
        returns_portfolio = returns_full[portfolio_symbols]

        # -----------------------------
        # Step 4: Compute weights (only for available assets)
        # -----------------------------
        total_value = self.portfolio.total_value()
        total_invested = sum(asset.amount_invested for asset in self.portfolio.assets)
        return_rate = ((total_value - total_invested) / total_invested) if total_invested else 0

        # Filter assets to only those with available data
        available_assets = [
            asset for asset in self.portfolio.assets
            if asset.symbol in portfolio_symbols
        ]

        weights = [
            asset.current_value / total_value
            for asset in available_assets
        ]

        # Renormalize weights to sum to 1
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]

        # -----------------------------
        # Step 5: Portfolio metrics
        # -----------------------------
        allocation = calculate_allocation(self.portfolio)

        # FIXED: pass aligned returns only
        volatility = portfolio_volatility(
            weights,
            returns_portfolio.cov().values
        )

        diversification = diversification_score(self.portfolio)

        # -----------------------------
        # Step 6: Market regime
        # -----------------------------
        market_data = self.market_engine.fetch_market_data()
        market_context = self.market_engine.detect_regime(market_data)

        # -----------------------------
        # Step 7: Risk scoring
        # -----------------------------
        risk_score = self.compute_risk_score(
            volatility,
            allocation,
            diversification,
            market_context,
            return_rate
        )

        risk_level = self.get_risk_level(risk_score)

        # -----------------------------
        # Step 8: Insights
        # -----------------------------
        insights = self.generate_insights(
            allocation,
            volatility,
            diversification,
            market_context,
            return_rate
        )

        # -----------------------------
        # Step 9: Recommendations
        # -----------------------------
        recommendations = self.recommendation_engine.generate_recommendations(
            allocation,
            volatility,
            market_context
        )

        # -----------------------------
        # Step 10: Sector exposure
        # -----------------------------
        sector_exposure = calculate_sector_exposure(self.portfolio)

        # -----------------------------
        # Step 11: Optimization (use full universe)
        # -----------------------------
        optimal_allocation = self.optimizer.optimize(returns_full)

        # Convert to dict for easier access
        optimal_allocation = {
            asset: weight
            for asset, weight in zip(optimal_allocation["assets"], optimal_allocation["weights"])
        }

        # -----------------------------
        # Final Output
        # -----------------------------
        return {
            "portfolio_value": total_value,
            "allocation": allocation,
            "sector_exposure": sector_exposure,
            "volatility": round(volatility * 100, 2),
            "return_rate": round(return_rate * 100, 2),
            "optimal_allocation": optimal_allocation,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "diversification_score": diversification,
            "market_context": market_context,
            "insights": insights,
            "recommendations": recommendations
        }

    def compute_risk_score(self, volatility, allocation, diversification, market_context, return_rate):
        """
        Compute a composite risk score based on multiple factors
        """
        # Base score from volatility (0-100 scale)
        vol_score = min(100, volatility * 100 * 5)  # Scale volatility to 0-100

        # Market regime adjustment
        regime = market_context.get("market_regime", "neutral")
        regime_multiplier = {
            "bull": 0.8,
            "neutral": 1.0,
            "bear": 1.3,
            "volatile": 1.5
        }.get(regime, 1.0)

        # Diversification bonus
        div_bonus = diversification * 0.5

        # Crypto exposure penalty
        crypto_penalty = allocation.get("crypto", 0) * 2

        # Performance adjustment: penalize losses, reward gains
        if return_rate < 0:
            performance_adjustment = abs(return_rate) * 25
        else:
            performance_adjustment = -min(return_rate, 0.2) * 10

        risk_score = (vol_score * regime_multiplier) - div_bonus + crypto_penalty + performance_adjustment
        return max(0, min(100, risk_score))

    def get_risk_level(self, risk_score):
        """
        Convert risk score to categorical risk level
        """
        if risk_score < 20:
            return "Very Low"
        elif risk_score < 40:
            return "Low"
        elif risk_score < 60:
            return "Moderate"
        elif risk_score < 80:
            return "High"
        else:
            return "Very High"

    def generate_insights(self, allocation, volatility, diversification, market_context, return_rate):
        """
        Generate key insights about the portfolio
        """
        insights = []

        # Volatility insight
        if volatility > 0.25:
            insights.append("Portfolio shows high volatility - consider defensive assets")
        elif volatility < 0.10:
            insights.append("Portfolio has low volatility - good for risk-averse investors")

        # Diversification insight
        if diversification < 50:
            insights.append("Limited diversification - consider adding more asset classes")
        else:
            insights.append("Well-diversified portfolio across multiple asset classes")

        # Performance insight
        if return_rate < 0:
            insights.append(f"Portfolio is currently down {abs(return_rate * 100):.2f}% - review underperforming positions")
        elif return_rate > 0:
            insights.append(f"Portfolio is currently up {return_rate * 100:.2f}%")
        else:
            insights.append("Portfolio is flat relative to invested capital")

        # Market context insight
        regime = market_context.get("market_regime", "neutral")
        if regime == "bull":
            insights.append("Bull market detected - consider increasing equity exposure")
        elif regime == "bear":
            insights.append("Bear market detected - consider defensive positioning")

        # Allocation insights
        crypto_pct = allocation.get("crypto", 0)
        if crypto_pct > 20:
            insights.append("High crypto exposure - monitor closely for volatility")

        return insights