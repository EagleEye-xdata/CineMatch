# CineMatch - Streamlit Setup

## Project Structure

```text
Movie_Recommendation_System_using_ML-main/
├── app.py
├── requirements.txt
├── SETUP.md
├── README.md
├── movies.csv
├── Movie_Recommendation_System.ipynb
├── recommendation/
│   ├── engine.py
│   ├── search.py
│   ├── filters.py
│   ├── hybrid.py
│   └── explainability.py
├── utils/
│   ├── data_loader.py
│   ├── helpers.py
│   ├── metrics.py
│   └── ratings_store.py
├── pages/
│   ├── 1_Recommendations.py
│   ├── 2_Analytics.py
│   └── 3_User_Ratings.py
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   └── placeholders/
└── data/
    └── user_ratings.csv
```

## What Was Preserved

The recommendation engine keeps the original notebook workflow:

- Load `movies.csv`
- Use `genres`, `keywords`, `tagline`, `cast`, and `director`
- Fill missing selected feature values with empty strings
- Combine selected text features
- Vectorize with `TfidfVectorizer`
- Calculate cosine similarity with `cosine_similarity`
- Use close title matching for misspelled movie searches

## Run Locally

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

If the Windows `python` command opens the Microsoft Store or says Python is not found, use `py`. The required dependencies have been installed into the system Python that the `py` launcher uses.

## Notes

The dataset does not include poster URLs. The Streamlit app uses styled poster placeholders so the UI stays clean without requiring an external API key.
