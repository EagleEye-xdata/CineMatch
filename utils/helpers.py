from __future__ import annotations

import html
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_css() -> None:
    css_path = PROJECT_ROOT / "assets" / "css" / "style.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def movie_card(movie, score_label: str | None = None) -> None:
    title = html.escape(str(movie.get("title", "Untitled")))
    genres = html.escape(str(movie.get("genres", "Unknown genre")))
    year = int(movie.get("release_year", 0) or 0)
    rating = float(movie.get("vote_average", 0) or 0)
    overview = html.escape(str(movie.get("overview", "No overview available."))[:220])
    score = f"<span>{score_label}</span>" if score_label else ""
    year_text = year if year else "N/A"

    st.markdown(
        f"""
        <div class="movie-card">
          <div class="poster-fallback">{title[:2].upper()}</div>
          <div class="movie-body">
            <div class="movie-title">{title}</div>
            <div class="movie-meta">{year_text} | {genres}</div>
            <div class="movie-overview">{overview}</div>
            <div class="movie-footer">
              <span>Rating {rating:.1f}/10</span>
              {score}
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
