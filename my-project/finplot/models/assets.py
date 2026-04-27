from dataclasses import dataclass

@dataclass
class Asset:
    symbol: str
    asset_type: str
    amount_invested: float
    current_value: float