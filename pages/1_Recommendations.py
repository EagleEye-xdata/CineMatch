from __future__ import annotations

import streamlit as st

from recommendation.engine import RecommendationEngine
from recommendation.explainability import explain_recommendation
from recommendation.filters import apply_filters
from recommendation.hybrid import add_hybrid_score
from recommendation.search import autocomplete_titles, find_close_title
from utils.data_loader import available_genres, available_languages, load_movies
from utils.helpers import load_css, movie_card
from utils.metrics import precision_at_k, recommendation_quality
from utils.ratings_store import load_ratings


st.set_page_config(page_title="CineMatch Recommendations", page_icon="target", layout="wide")


@st.cache_data(show_spinner=False)
def cached_movies():
    return load_movies()


@st.cache_resource(show_spinner=False)
def cached_engine(movies):
    return RecommendationEngine.build(movies)


movies = cached_movies()
engine = cached_engine(movies)
ratings = load_ratings()
load_css()

st.title("Recommendations")

default_title = st.session_state.get("selected_movie", "")
query = st.text_input("Movie title", value=default_title, placeholder="Search a movie")
suggestions = autocomplete_titles(query, movies) if query else []
selected_title = st.selectbox("Autocomplete suggestions", suggestions) if suggestions else query

with st.sidebar:
    st.header("Filters")
    mode = st.radio(
        "Recommendation mode",
        ["Content-based", "Popularity-based", "Hybrid"],
    )
    genre = st.selectbox("Genre", ["All"] + available_genres(movies))
    years = movies[movies["release_year"] > 0]["release_year"]
    year_range = st.slider(
        "Release year",
        int(years.min()),
        int(years.max()),
        (int(years.min()), int(years.max())),
    )
    min_rating = st.slider("Minimum rating", 0.0, 10.0, 0.0, 0.5)
    language = st.selectbox("Language", ["All"] + available_languages(movies))
    limit = st.slider("Number of results", 5, 30, 12)

if not selected_title:
    st.markdown(
        '<div class="empty-state">Search for a movie to see recommendations.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

matched_title = find_close_title(selected_title, movies)
if not matched_title:
    st.error("No matching movie found. Try another title.")
    st.stop()

source_index = engine.get_movie_index(matched_title)
if source_index is None:
    st.error("The matched movie exists in the dataset but could not be indexed.")
    st.stop()

source_movie = movies.iloc[source_index]
st.caption(f"Showing results for: {matched_title}")

if mode == "Popularity-based":
    recommendations = engine.popular_movies(limit=100)
    recommendations["similarity_score"] = 0.0
else:
    with st.spinner("Calculating cosine similarity recommendations..."):
        recommendations = engine.recommend_by_index(source_index, limit=100)
    if mode == "Hybrid":
        recommendations = add_hybrid_score(recommendations, ratings)

recommendations = apply_filters(
    recommendations,
    genre=genre,
    year_range=year_range,
    min_rating=min_rating,
    language=language,
).head(limit)

if recommendations.empty:
    st.markdown(
        '<div class="empty-state">No recommendations match the selected filters.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

quality = recommendation_quality(recommendations)
metric_cols = st.columns(4)
metric_cols[0].metric("Avg similarity", quality["avg_similarity"])
metric_cols[1].metric("Avg rating", quality["avg_rating"])
metric_cols[2].metric("Avg popularity", quality["avg_popularity"])
metric_cols[3].metric("Precision@10", precision_at_k(recommendations))

st.divider()

for _, movie in recommendations.iterrows():
    score = movie.get("hybrid_score", movie.get("similarity_score", 0.0))
    label = "Score " + f"{float(score):.3f}"
    movie_card(movie, score_label=label)
    with st.expander("Why was this movie recommended?"):
        for reason in explain_recommendation(source_movie, movie):
            st.write(reason)
