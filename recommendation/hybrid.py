from __future__ import annotations

import pandas as pd


def add_hybrid_score(
    recommendations: pd.DataFrame,
    user_ratings: pd.DataFrame | None = None,
) -> pd.DataFrame:
    scored = recommendations.copy()
    if scored.empty:
        return scored

    similarity = scored.get("similarity_score", 0)
    popularity = scored["popularity"] / max(float(scored["popularity"].max()), 1.0)
    rating = scored["vote_average"] / 10

    scored["hybrid_score"] = similarity * 0.65 + popularity * 0.2 + rating * 0.15

    if user_ratings is not None and not user_ratings.empty:
        liked_titles = user_ratings[user_ratings["rating"] >= 4]["title"].tolist()
        if liked_titles:
            liked_genres = " ".join(
                scored[scored["title"].isin(liked_titles)]["genres"].tolist()
            ).split()
            if liked_genres:
                liked_set = set(liked_genres)
                scored["hybrid_score"] += scored["genres"].apply(
                    lambda value: 0.05
                    * len(set(str(value).split()).intersection(liked_set))
                )

    return scored.sort_values("hybrid_score", ascending=False)

