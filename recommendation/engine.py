from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SELECTED_FEATURES = ["genres", "keywords", "tagline", "cast", "director"]


@dataclass
class RecommendationEngine:
    """Content-based recommender based on the original notebook workflow."""

    movies: pd.DataFrame
    vectorizer: TfidfVectorizer
    feature_vectors: object
    similarity: object

    @classmethod
    def build(cls, movies: pd.DataFrame) -> "RecommendationEngine":
        movies = movies.copy()

        for feature in SELECTED_FEATURES:
            movies[feature] = movies[feature].fillna("")

        combined_features = (
            movies["genres"]
            + " "
            + movies["keywords"]
            + " "
            + movies["tagline"]
            + " "
            + movies["cast"]
            + " "
            + movies["director"]
        )

        vectorizer = TfidfVectorizer()
        feature_vectors = vectorizer.fit_transform(combined_features)
        similarity = cosine_similarity(feature_vectors)

        return cls(
            movies=movies,
            vectorizer=vectorizer,
            feature_vectors=feature_vectors,
            similarity=similarity,
        )

    def recommend_by_index(self, movie_index: int, limit: int = 12) -> pd.DataFrame:
        scores = list(enumerate(self.similarity[movie_index]))
        sorted_scores = sorted(scores, key=lambda item: item[1], reverse=True)
        rows = []

        for index, score in sorted_scores:
            if index == movie_index:
                continue
            row = self.movies.iloc[index].copy()
            row["similarity_score"] = float(score)
            rows.append(row)
            if len(rows) >= limit:
                break

        return pd.DataFrame(rows)

    def get_movie_index(self, title: str) -> int | None:
        matches = self.movies.index[
            self.movies["title"].str.lower() == title.strip().lower()
        ].tolist()
        return int(matches[0]) if matches else None

    def popular_movies(self, limit: int = 12) -> pd.DataFrame:
        return (
            self.movies.sort_values(
                ["popularity", "vote_average", "vote_count"], ascending=False
            )
            .head(limit)
            .copy()
        )

    def trending_movies(self, limit: int = 12) -> pd.DataFrame:
        recent = self.movies[self.movies["release_year"] >= 2010].copy()
        if recent.empty:
            recent = self.movies.copy()
        recent["trend_score"] = (
            recent["popularity"] * 0.6
            + recent["vote_average"] * 8
            + recent["vote_count"].clip(upper=5000) / 500
        )
        return recent.sort_values("trend_score", ascending=False).head(limit).copy()

