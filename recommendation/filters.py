from __future__ import annotations

import pandas as pd


def apply_filters(
    movies: pd.DataFrame,
    genre: str | None = None,
    year_range: tuple[int, int] | None = None,
    min_rating: float = 0.0,
    language: str | None = None,
) -> pd.DataFrame:
    filtered = movies.copy()

    if genre and genre != "All":
        filtered = filtered[filtered["genres"].str.contains(genre, case=False, na=False)]

    if year_range:
        start_year, end_year = year_range
        filtered = filtered[
            (filtered["release_year"] >= start_year)
            & (filtered["release_year"] <= end_year)
        ]

    if min_rating:
        filtered = filtered[filtered["vote_average"] >= min_rating]

    if language and language != "All":
        filtered = filtered[filtered["original_language"] == language]

    return filtered

