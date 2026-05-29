from __future__ import annotations

import difflib
import re

import pandas as pd


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", value.lower()).strip()


def _title_score(query: str, title: str) -> float:
    normalized_query = _normalize(query)
    normalized_title = _normalize(title)
    query_tokens = _canonical_tokens(normalized_query)
    title_tokens = _canonical_tokens(normalized_title)

    if not normalized_query or not normalized_title:
        return 0.0

    full_ratio = difflib.SequenceMatcher(
        None, normalized_query, normalized_title
    ).ratio()
    partial_ratio = (
        1.0 if normalized_query in normalized_title else 0.0
    )

    token_scores = []
    for query_token in query_tokens:
        best_token_score = max(
            difflib.SequenceMatcher(None, query_token, title_token).ratio()
            for title_token in title_tokens
        )
        token_scores.append(best_token_score)

    token_ratio = sum(token_scores) / len(token_scores)
    token_overlap = len(set(query_tokens).intersection(title_tokens)) / max(
        len(set(query_tokens)), 1
    )

    return full_ratio * 0.35 + partial_ratio * 0.15 + token_ratio * 0.35 + token_overlap * 0.15


def _canonical_tokens(value: str) -> list[str]:
    aliases = {
        "nite": "knight",
        "night": "knight",
    }
    stopwords = {"a", "an", "the"}
    return [
        aliases.get(token, token)
        for token in value.split()
        if token and token not in stopwords
    ]


def find_close_title(query: str, movies: pd.DataFrame) -> str | None:
    titles = movies["title"].dropna().astype(str).tolist()
    ranked = sorted(
        ((title, _title_score(query, title)) for title in titles),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked[0][0] if ranked and ranked[0][1] >= 0.35 else None


def autocomplete_titles(query: str, movies: pd.DataFrame, limit: int = 8) -> list[str]:
    titles = movies["title"].dropna().astype(str).tolist()
    if not query.strip():
        return titles[:limit]

    query_lower = query.lower().strip()
    starts_with = [title for title in titles if title.lower().startswith(query_lower)]
    contains = [
        title
        for title in titles
        if query_lower in title.lower() and title not in starts_with
    ]
    fuzzy = [
        title
        for title, score in sorted(
            ((title, _title_score(query, title)) for title in titles),
            key=lambda item: item[1],
            reverse=True,
        )
        if score >= 0.25
    ][:limit]

    suggestions = []
    for title in starts_with + contains + fuzzy:
        if title not in suggestions:
            suggestions.append(title)
        if len(suggestions) >= limit:
            break

    return suggestions
