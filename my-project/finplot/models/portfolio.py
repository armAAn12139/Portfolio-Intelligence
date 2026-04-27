from dataclasses import dataclass
from typing import List
from models.assets import Asset

@dataclass
class Portfolio:
    assets: List[Asset]

    def total_value(self):
        return sum(asset.current_value for asset in self.assets)