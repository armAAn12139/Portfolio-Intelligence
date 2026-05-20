import json
from pathlib import Path
from typing import List

from models.assets import Asset

ROOT_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = ROOT_DIR / "saved_portfolios"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def get_portfolio_path(name: str) -> Path:
    return STORAGE_DIR / f"{name}.json"


def list_saved_portfolios() -> List[str]:
    return sorted(path.stem for path in STORAGE_DIR.glob("*.json"))


def save_portfolio(name: str, assets: List[Asset], description: str = "") -> Path:
    if not name or not name.strip():
        raise ValueError("Portfolio name must be provided")

    payload = {
        "name": name.strip(),
        "description": description,
        "assets": [asset.to_dict() for asset in assets],
    }

    path = get_portfolio_path(payload["name"])
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    return path


def load_portfolio(name: str) -> List[Asset]:
    path = get_portfolio_path(name)
    if not path.exists():
        raise FileNotFoundError(f"Saved portfolio not found: {name}")

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    return [Asset.from_dict(item) for item in payload.get("assets", [])]


def delete_portfolio(name: str) -> bool:
    path = get_portfolio_path(name)
    if path.exists():
        path.unlink()
        return True
    return False


def export_portfolio_json(assets: List[Asset], name: str = "portfolio") -> str:
    payload = {
        "name": name or "portfolio",
        "assets": [asset.to_dict() for asset in assets],
    }
    return json.dumps(payload, indent=2)
