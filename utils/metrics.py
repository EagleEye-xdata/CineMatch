from __future__ import annotations

import pandas as pd


def dataset_stats(movies: pd.DataFrame) -> dict[str, object]:
    years = movies[movies["release_year"] > 0]["release_year"]
    return {
        "movies": len(movies),
        "genres": len({g for value in movies["genres"] for g in str(value).split()}),
        "languages": movies["original_language"].nunique(),
        "year_range": f"{int(years.min())} - {int(years.max())}" if not years.empty else "N/A",
        "average_rating": round(float(movies["vote_average"].mean()), 2),
    }


def recommendation_quality(recommendations: pd.DataFrame) -> dict[str, float]:
    if recommendations.empty:
        return {"avg_similarity": 0.0, "avg_rating": 0.0, "avg_popularity": 0.0}
    return {
        "avg_similarity": round(float(recommendations["similarity_score"].mean()), 3),
        "avg_rating": round(float(recommendations["vote_average"].mean()), 2),
        "avg_popularity": round(float(recommendations["popularity"].mean()), 2),
    }


def precision_at_k(recommendations: pd.DataFrame, min_rating: float = 7.0, k: int = 10) -> float:
    top_k = recommendations.head(k)
    if top_k.empty:
        return 0.0
    relevant = top_k[top_k["vote_average"] >= min_rating]
    return round(len(relevant) / len(top_k), 3)

