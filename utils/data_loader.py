from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_PATH = PROJECT_ROOT / "movies.csv"


def load_movies(path: str | Path = DEFAULT_DATASET_PATH) -> pd.DataFrame:
    """Load the existing movies dataset and prepare display-friendly fields."""
    movies = pd.read_csv(path)
    movies = movies.copy()

    if "index" not in movies.columns:
        movies["index"] = movies.index

    for column in [
        "genres",
        "keywords",
        "tagline",
        "cast",
        "director",
        "overview",
        "title",
        "original_language",
    ]:
        if column in movies.columns:
            movies[column] = movies[column].fillna("")

    movies["release_year"] = pd.to_datetime(
        movies.get("release_date"), errors="coerce"
    ).dt.year
    movies["release_year"] = movies["release_year"].fillna(0).astype(int)
    movies["vote_average"] = pd.to_numeric(
        movies.get("vote_average", 0), errors="coerce"
    ).fillna(0.0)
    movies["vote_count"] = pd.to_numeric(
        movies.get("vote_count", 0), errors="coerce"
    ).fillna(0)
    movies["popularity"] = pd.to_numeric(
        movies.get("popularity", 0), errors="coerce"
    ).fillna(0.0)

    return movies


def available_genres(movies: pd.DataFrame) -> list[str]:
    genres: set[str] = set()
    for value in movies["genres"].fillna(""):
        genres.update(part.strip() for part in value.split() if part.strip())
    return sorted(genres)


def available_languages(movies: pd.DataFrame) -> list[str]:
    languages = movies["original_language"].fillna("").astype(str).str.strip()
    return sorted(language for language in languages.unique() if language)

