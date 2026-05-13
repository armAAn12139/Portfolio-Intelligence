from dataclasses import dataclass
from typing import List
from models.assets import Asset
from utils.currency_converter import converter

@dataclass
class Portfolio:
    assets: List[Asset]

    def total_value(self):
        """Total portfolio value in INR"""
        return sum(converter.convert_to_inr(asset.current_value, asset.currency) for asset in self.assets)

    def total_invested(self):
        """Total amount invested in INR"""
        return sum(converter.convert_to_inr(asset.amount_invested, asset.currency) for asset in self.assets)