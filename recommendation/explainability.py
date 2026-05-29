from __future__ import annotations

import pandas as pd


def _tokens(value: object) -> set[str]:
    return {token.strip().lower() for token in str(value).split() if token.strip()}


def explain_recommendation(source: pd.Series, recommended: pd.Series) -> list[str]:
    reasons: list[str] = []

    shared_genres = _tokens(source.get("genres", "")).intersection(
        _tokens(recommended.get("genres", ""))
    )
    shared_keywords = _tokens(source.get("keywords", "")).intersection(
        _tokens(recommended.get("keywords", ""))
    )
    shared_cast = _tokens(source.get("cast", "")).intersection(
        _tokens(recommended.get("cast", ""))
    )

    if shared_genres:
        reasons.append("Similar genres: " + ", ".join(sorted(shared_genres)[:4]))
    if shared_keywords:
        reasons.append("Shared keywords: " + ", ".join(sorted(shared_keywords)[:4]))
    if shared_cast:
        reasons.append("Similar cast signals: " + ", ".join(sorted(shared_cast)[:4]))
    if source.get("director") and source.get("director") == recommended.get("director"):
        reasons.append("Same director: " + str(source.get("director")))

    return reasons or ["Strong textual similarity across movie metadata."]

