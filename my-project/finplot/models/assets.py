from dataclasses import dataclass

@dataclass
class Asset:
    symbol: str
    asset_type: str
    amount_invested: float
    current_value: float
    currency: str = "INR"  # Default to INR

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "asset_type": self.asset_type,
            "amount_invested": self.amount_invested,
            "current_value": self.current_value,
            "currency": self.currency,
        }

    @staticmethod
    def from_dict(data: dict) -> "Asset":
        return Asset(
            symbol=data.get("symbol", ""),
            asset_type=data.get("asset_type", "stock"),
            amount_invested=float(data.get("amount_invested", 0.0)) if data.get("amount_invested", None) is not None else 0.0,
            current_value=float(data.get("current_value", 0.0)) if data.get("current_value", None) is not None else 0.0,
            currency=data.get("currency", "INR") or "INR",
        )