class RecommendationEngine:

    def generate_recommendations(self, allocation, volatility, market_context):

        recommendations = []

        market_regime = market_context.get("market_regime", "Unknown")

        # Risk-based recommendations
        if volatility > 0.20:
            recommendations.append(
                "Consider reducing exposure to highly volatile assets to lower overall portfolio risk."
            )

        # Crypto allocation check
        crypto_exposure = allocation.get("BTC-USD", 0)

        if crypto_exposure > 15:
            recommendations.append(
                "Crypto allocation exceeds recommended levels. Consider reducing exposure to below 10–15%."
            )

        # Tech concentration check
        tech_weight = allocation.get("AAPL", 0) + allocation.get("MSFT", 0)

        if tech_weight > 50:
            recommendations.append(
                "Technology sector exposure is high. Diversifying into other sectors may improve stability."
            )

        # Market regime recommendations
        if market_regime == "High Volatility":
            recommendations.append(
                "Market volatility is elevated. Increasing defensive assets like gold or bonds may help reduce risk."
            )

        if market_regime == "Bull Market":
            recommendations.append(
                "Markets are trending upward. Growth assets such as equities may provide better returns."
            )

        if market_regime == "Bear Market":
            recommendations.append(
                "Bearish conditions detected. Consider increasing cash or defensive assets."
            )

        return recommendations