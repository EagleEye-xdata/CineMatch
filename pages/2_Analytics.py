from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.data_loader import load_movies
from utils.helpers import load_css
from utils.metrics import dataset_stats


st.set_page_config(page_title="Analytics", page_icon="bar_chart", layout="wide")


@st.cache_data(show_spinner=False)
def cached_movies():
    return load_movies()


movies = cached_movies()
load_css()

st.title("Analytics")

stats = dataset_stats(movies)
cols = st.columns(5)
cols[0].metric("Movies", f"{stats['movies']:,}")
cols[1].metric("Genres", stats["genres"])
cols[2].metric("Languages", stats["languages"])
cols[3].metric("Years", stats["year_range"])
cols[4].metric("Avg rating", stats["average_rating"])

st.divider()

left, right = st.columns(2, gap="large")

with left:
    st.subheader("Popular genres")
    genre_counts = (
        pd.Series(" ".join(movies["genres"].fillna("").astype(str)).split())
        .value_counts()
        .head(15)
    )
    st.bar_chart(genre_counts)

with right:
    st.subheader("Language distribution")
    language_counts = movies["original_language"].value_counts().head(15)
    st.bar_chart(language_counts)

left, right = st.columns(2, gap="large")

with left:
    st.subheader("Rating distribution")
    rating_bins = pd.cut(movies["vote_average"], bins=10).value_counts().sort_index()
    rating_bins.index = rating_bins.index.astype(str)
    st.bar_chart(rating_bins)

with right:
    st.subheader("Movies by decade")
    decade_data = movies[movies["release_year"] > 0].copy()
    decade_data["decade"] = (decade_data["release_year"] // 10) * 10
    st.bar_chart(decade_data["decade"].value_counts().sort_index())

st.subheader("Top movies by popularity")
st.dataframe(
    movies.sort_values("popularity", ascending=False)[
        ["title", "genres", "release_year", "vote_average", "popularity"]
    ].head(20),
    use_container_width=True,
)
