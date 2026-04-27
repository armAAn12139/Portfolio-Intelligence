import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class RiskScorer:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=6,
            random_state=42
        )
        self.is_trained = False

    # -----------------------------
    # Feature Engineering
    # -----------------------------
    def compute_features(self, portfolio, market_data):
        """
        portfolio: dict
        market_data: dict

        Returns: feature vector (list)
        """

        # Portfolio features
        volatility = portfolio.get("volatility", 0)
        sharpe_ratio = portfolio.get("sharpe_ratio", 0)
        max_drawdown = portfolio.get("max_drawdown", 0)
        tech_exposure = portfolio.get("tech_exposure", 0)
        diversification_score = portfolio.get("diversification_score", 0)

        # Market features
        vix = market_data.get("vix", 15)
        inflation = market_data.get("inflation", 5)
        interest_rate = market_data.get("interest_rate", 6)
        market_trend = market_data.get("market_trend", 0)  # -1 bearish, 0 neutral, 1 bullish

        return [
            volatility,
            sharpe_ratio,
            max_drawdown,
            tech_exposure,
            diversification_score,
            vix,
            inflation,
            interest_rate,
            market_trend
        ]

    # -----------------------------
    # Training (offline / batch)
    # -----------------------------
    def train(self, X, y):
        """
        X: feature matrix
        y: risk scores (0–100)
        """
        self.model.fit(X, y)
        self.is_trained = True

    # -----------------------------
    # Prediction
    # -----------------------------
    def predict_risk(self, portfolio, market_data):
        """
        Returns:
        {
            risk_score: int,
            risk_category: str,
            drawdown_probability: float
        }
        """

        features = self.compute_features(portfolio, market_data)
        features = np.array(features).reshape(1, -1)

        if self.is_trained:
            risk_score = self.model.predict(features)[0]
        else:
            # fallback heuristic (IMPORTANT for MVP)
            risk_score = self.rule_based_score(portfolio, market_data)

        risk_score = int(np.clip(risk_score, 0, 100))

        return {
            "risk_score": risk_score,
            "risk_category": self.get_risk_category(risk_score),
            "drawdown_probability": self.estimate_drawdown(risk_score)
        }

    # -----------------------------
    # Rule-based fallback (MVP)
    # -----------------------------
    def rule_based_score(self, portfolio, market_data):
        score = 0

        # Portfolio risk
        score += portfolio.get("volatility", 0) * 0.3
        score += portfolio.get("max_drawdown", 0) * 0.2
        score -= portfolio.get("sharpe_ratio", 0) * 5

        # Concentration risk
        if portfolio.get("tech_exposure", 0) > 40:
            score += 10

        if portfolio.get("diversification_score", 0) < 50:
            score += 15

        # Market risk
        score += market_data.get("vix", 15) * 0.5
        score += market_data.get("inflation", 5) * 1.2

        if market_data.get("market_trend", 0) == -1:
            score += 10

        return score

    # -----------------------------
    # Risk Bucketing
    # -----------------------------
    def get_risk_category(self, score):
        if score < 30:
            return "Low"
        elif score < 60:
            return "Moderate"
        else:
            return "High"

    # -----------------------------
    # Drawdown Estimation
    # -----------------------------
    def estimate_drawdown(self, risk_score):
        """
        Simple probabilistic mapping
        """
        return round(min(0.05 + (risk_score / 200), 0.8), 2)