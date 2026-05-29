from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RATINGS_PATH = PROJECT_ROOT / "data" / "user_ratings.csv"


def load_ratings(path: Path = RATINGS_PATH) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["title", "rating", "notes"])
    return pd.read_csv(path)


def save_rating(title: str, rating: int, notes: str = "", path: Path = RATINGS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ratings = load_ratings(path)
    ratings = ratings[ratings["title"] != title]
    new_row = pd.DataFrame([{"title": title, "rating": rating, "notes": notes}])
    ratings = pd.concat([ratings, new_row], ignore_index=True)
    ratings.to_csv(path, index=False)

