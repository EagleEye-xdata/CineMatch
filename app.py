from __future__ import annotations

import streamlit as st

from recommendation.engine import RecommendationEngine
from recommendation.search import autocomplete_titles, find_close_title
from utils.data_loader import load_movies
from utils.helpers import load_css, movie_card


st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="movie_camera",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def cached_movies():
    return load_movies()


@st.cache_resource(show_spinner=False)
def cached_engine(movies):
    return RecommendationEngine.build(movies)


movies = cached_movies()
engine = cached_engine(movies)
load_css()

st.markdown('<div class="app-title">Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Content-based movie discovery powered by your existing TF-IDF and cosine similarity workflow.</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1.25, 0.75], gap="large")

with left:
    st.subheader("Find a movie")
    query = st.text_input(
        "Search by title",
        placeholder="Try The Dark Knight, Avatar, Iron Man...",
        label_visibility="collapsed",
    )

    suggestions = autocomplete_titles(query, movies) if query else []
    selected_title = None
    if suggestions:
        selected_title = st.selectbox("Suggestions", suggestions)

    if st.button("Get recommendations", type="primary", use_container_width=True):
        chosen_title = selected_title or find_close_title(query, movies)
        if chosen_title:
            st.session_state["selected_movie"] = chosen_title
            st.switch_page("pages/1_Recommendations.py")
        else:
            st.error("No close movie title found. Try another spelling or a shorter title.")

with right:
    st.subheader("Dataset snapshot")
    metric_cols = st.columns(2)
    metric_cols[0].metric("Movies", f"{len(movies):,}")
    metric_cols[1].metric("Languages", movies["original_language"].nunique())
    metric_cols[0].metric("Avg rating", f"{movies['vote_average'].mean():.1f}/10")
    metric_cols[1].metric("Years", f"{movies[movies['release_year'] > 0]['release_year'].min()}-{movies['release_year'].max()}")

st.divider()

st.subheader("Trending recommendations")
trending = engine.trending_movies(limit=6)
trend_cols = st.columns(2)
for idx, (_, movie) in enumerate(trending.iterrows()):
    with trend_cols[idx % 2]:
        movie_card(movie)

st.subheader("Popular movies")
popular = engine.popular_movies(limit=6)
popular_cols = st.columns(2)
for idx, (_, movie) in enumerate(popular.iterrows()):
    with popular_cols[idx % 2]:
        movie_card(movie)
