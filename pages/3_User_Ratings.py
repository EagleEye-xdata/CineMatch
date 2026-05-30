from __future__ import annotations

import streamlit as st

from utils.data_loader import load_movies
from utils.helpers import load_css
from utils.ratings_store import load_ratings, save_rating


st.set_page_config(page_title="CineMatch User Ratings", page_icon="star", layout="wide")


@st.cache_data(show_spinner=False)
def cached_movies():
    return load_movies()


movies = cached_movies()
load_css()

st.title("User Ratings")
st.caption("Ratings are saved locally in data/user_ratings.csv and used by hybrid recommendations.")

title = st.selectbox("Movie", movies["title"].tolist())
rating = st.slider("Your rating", 1, 5, 4)
notes = st.text_area("Notes", placeholder="Optional notes about why you liked or disliked it")

if st.button("Save rating", type="primary"):
    save_rating(title, rating, notes)
    st.success("Rating saved.")

st.divider()

ratings = load_ratings()
if ratings.empty:
    st.markdown(
        '<div class="empty-state">No user ratings saved yet.</div>',
        unsafe_allow_html=True,
    )
else:
    st.subheader("Saved ratings")
    st.dataframe(ratings.sort_values("rating", ascending=False), use_container_width=True)
