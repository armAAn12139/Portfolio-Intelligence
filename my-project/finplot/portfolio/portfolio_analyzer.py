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
        unavailable_symbols = [s for s in portfolio_symbols if s not in available_symbols]
        portfolio_symbols = [s for s in portfolio_symbols if s in available_symbols]

        if not portfolio_symbols:
            error_msg = f"No market data available for portfolio assets. Missing: {', '.join(unavailable_symbols) if unavailable_symbols else 'All symbols'}"
            raise ValueError(error_msg)
        
        # Warn about unavailable symbols
        if unavailable_symbols:
            print(f"⚠️  Warning: Could not fetch data for symbols: {', '.join(unavailable_symbols)}")
            print(f"   These assets may be delisted or have no data. Analyzing {len(portfolio_symbols)} available asset(s).")

        returns_full = calculate_returns(price_data_full)

        # -----------------------------
        # Step 3: Create portfolio-only returns (CRITICAL FIX)
        # -----------------------------
        returns_portfolio = returns_full[portfolio_symbols]

        # -----------------------------
        # Step 4: Compute weights (only for available assets)
        # -----------------------------
        total_value = self.portfolio.total_value()
        total_invested = self.portfolio.total_invested()
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
        Weighted components:
        - Volatility: 40%
        - Concentration: 25%
        - Market regime: 20%
        - Return performance: 15%
        """
        # Base score from volatility (stronger weighting)
        # volatility is in decimal form (0.20 = 20%)
        vol_score = min(100, volatility * 100 * 5.5)  # Slightly increased multiplier
        
        # Concentration risk from allocation
        concentration_risk = 0
        single_asset_max = max(allocation.values()) if allocation else 0
        concentration_risk = single_asset_max * 1.2  # Penalize concentration
        
        if single_asset_max > 30:  # More than 30% in single asset
            concentration_risk += 20
        if single_asset_max > 50:  # More than 50% in single asset
            concentration_risk += 30

        # Market regime adjustment (with stronger impact)
        regime = market_context.get("market_regime", "neutral")
        regime_multiplier = {
            "bull": 0.9,      # Slightly reduced
            "neutral": 1.0,
            "bear": 1.4,      # Increased
            "volatile": 1.8   # Significantly increased
        }.get(regime, 1.0)

        # Diversification penalty (increased impact for poor diversification)
        diversification_score_val = (100 - diversification) * 0.6  # Higher penalty for low diversity
        
        # Crypto exposure penalty (remains aggressive)
        crypto_penalty = allocation.get("crypto", 0) * 2.5

        # Performance adjustment (penalize significant losses more heavily)
        if return_rate < -0.20:  # -20% or worse
            performance_adjustment = abs(return_rate) * 40
        elif return_rate < 0:
            performance_adjustment = abs(return_rate) * 30
        else:
            performance_adjustment = -min(return_rate * 0.05, 5)  # Minimal reward for gains

        # Composite score with better weighting
        risk_score = (
            (vol_score * 0.40) +
            (concentration_risk * 0.25) +
            (vol_score * regime_multiplier * 0.20) +
            (diversification_score_val * 0.15) +
            crypto_penalty +
            performance_adjustment
        )
        
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