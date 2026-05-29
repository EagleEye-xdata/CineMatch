# 🎬 CineMatch: AI-Powered Movie Recommendation System

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io)
[![ML Framework](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg)](https://scikit-learn.org)

An advanced, multi-page, content-based movie recommendation system built using Machine Learning and NLP. It processes textual metadata (genres, keywords, taglines, cast, directors) using TF-IDF vectorization and Cosine Similarity, offering a premium interactive web experience complete with real-time explainability, advanced analytics, and persistent user rating profiles.

---

## 📌 Project Objective

The goal of CineMatch is to solve the **cold-start problem** in recommender systems. Instead of requiring historical user watch patterns or collaborative ratings, CineMatch leverages Natural Language Processing (NLP) to extract deep textual similarities directly from movie metadata. The application is designed to be highly interactive, transparent (Explainable AI), and visually stunning, matching industry-standard production applications.

---

## 🚀 Key Features

* 🔍 **Smart Content Search & Autocomplete**: Uses fuzzy string matching (`difflib`) to allow searching for movies with typos or incomplete titles.
* 🧠 **Explainable AI (XAI)**: Shows *why* a movie was recommended by visualizing overlapping metadata tags and text feature vector weights.
* 🎛️ **Hybrid Multi-Filters**: Refine recommendations by genres, minimum runtime, popularity range, and specific keywords.
* 📊 **Dynamic Data Analytics Dashboard**:
  * Distribution of movie popularity vs. average votes.
  * Runtime distribution histograms.
  * Interactive breakdown of the most popular genres.
  * Dataset summary statistics.
* 💾 **Persistent User Profiles & Ratings**: Rate movies directly in the app. Ratings are saved locally in a structured CSV file, dynamically updating your personalized recommended history.
* 🎨 **Premium Aesthetic**: Responsive sidebar, custom glassmorphism design, custom CSS styles, and responsive cards with detailed popovers.

---

## 🛠️ Tech Stack & Architecture

CineMatch is built as a highly modular, scalable, multi-page web application.

```text
┌───────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                     │
│    (app.py, page1: Recommendations, page2: Analytics,     │
│                   page3: User Ratings)                    │
└─────────────┬───────────────────────────────▲─────────────┘
              │ User Interactions             │ Rendered Data/Charts
              ▼                               │
┌─────────────────────────────────────────────┴─────────────┐
│                    Recommendation Core                    │
│      (Engine, Filters, Search, Explainability Module)      │
└─────────────┬───────────────────────────────▲─────────────┘
              │ Load Metadata / Tokenize      │ TF-IDF & Cosine Similarity
              ▼                               │
┌─────────────────────────────────────────────┴─────────────┐
│                       Data Layer                          │
│     (Pandas Loader, Local CSV Database: user_ratings.csv) │
└───────────────────────────────────────────────────────────┘
```

* **Frontend**: [Streamlit](https://streamlit.io/) (Multi-page App Structure)
* **Design & Styling**: Custom CSS stylesheets, Google Fonts (Outfit, Inter)
* **Natural Language Processing**: `TfidfVectorizer` (scikit-learn), text tokenization and metadata combination
* **Similarity Computation**: `cosine_similarity` (scikit-learn), NumPy matrix operations
* **Data Engineering**: Pandas, NumPy
* **Analytics & Visualizations**: Matplotlib, Seaborn, Streamlit native interactive charts

---

## 📂 Project Structure

```text
Movie_Recommendation_System_Streamlit/
├── app.py                      # Main landing page & application entrypoint
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive project documentation
├── SETUP.md                    # Setup guide
├── movies.csv                  # Core movie dataset (20,000+ movies)
├── Movie_Recommendation_System.ipynb # Original research/prototyping notebook
├── recommendation/             # Recommendation logic package
│   ├── __init__.py
│   ├── engine.py               # TF-IDF & Cosine Similarity computation
│   ├── search.py               # Fuzzy name matching and search utils
│   ├── filters.py              # Metadata genre/runtime/popularity filtering
│   ├── hybrid.py               # Hybrid scoring logic (popularity + similarity)
│   └── explainability.py       # XAI term overlap & explanation generator
├── utils/                      # Helper & backend utility package
│   ├── __init__.py
│   ├── data_loader.py          # Cached data loading & prep
│   ├── helpers.py              # Text formatting and display UI helpers
│   ├── metrics.py              # Recommendation score and math metrics
│   └── ratings_store.py        # Persistent user CSV reader/writer
├── pages/                      # Streamlit multi-page directory
│   ├── 1_Recommendations.py    # Main movie search & matching interface
│   ├── 2_Analytics.py          # Interactive dataset analytics dashboards
│   └── 3_User_Ratings.py       # Dynamic rating system & personalized history
├── assets/                     # Frontend static assets
│   ├── css/
│   │   └── style.css           # Premium dark-theme & glassmorphism stylesheet
│   └── placeholders/           # Static local placeholder assets
└── data/
    └── user_ratings.csv        # Local DB storing persistent user ratings
```

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.8 or higher installed on your computer.

### Step-by-Step Installation

1. **Clone your repository**:
   ```bash
   git clone https://github.com/EagleEye-xdata/Movie_Recommendation_System_Streamlit.git
   cd Movie_Recommendation_System_Streamlit
   ```

2. **Install all required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit web application**:
   ```bash
   streamlit run app.py
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:8501`.

---

## 🎙️ Loom Presentation & Live Demo Script

To make submitting your project as easy as possible, use this structured script to record your **Loom Video**:

### Section 1: Self-Introduction (30 Seconds)
> *"Hello, my name is [Your Name], and I am presenting **CineMatch**, an AI-powered content-based Movie Recommendation System. Today, I'll walk you through the problem statement, our machine learning approach, the technical architecture, and a live demonstration of the multi-page application."*

### Section 2: Problem Statement & ML Methodology (1 Minute)
> *"Standard recommendation engines face the cold-start problem where new users or fresh movies have no watch history to make collaborative recommendations. CineMatch solves this by using NLP.*
>
> *We combine key metadata features—such as genres, keywords, taglines, cast, and directors—into a unified textual profile for each movie. We tokenize this using a TF-IDF vectorizer to extract word importance, then compute a **Cosine Similarity Matrix** across all movies. When a movie is selected, we retrieve the top most similar vectors, providing robust, content-based recommendations instantly."*

### Section 3: Live Application Demo (1.5 Minutes)
1. **Landing Page**:
   > *"Here is our main dashboard. We have integrated custom glassmorphic styling, responsive sidebars, and clean navigation."*
2. **Recommendations Tab**:
   > *"Under the Recommendations tab, you can search for any movie. If we search for 'The Dark Knight', the fuzzy search handles any typos. The app displays the top recommendations. We also have an **Explainable AI** popup that shows exactly which terms (like 'superhero', 'batman', 'director: christopher nolan') led to this recommendation."*
3. **Analytics Tab**:
   > *"On our Analytics page, we provide deep insights into the dataset: genre distributions, popularity vs. ratings, and average runtimes, showing how our dataset is structured."*
4. **User Ratings Tab**:
   > *"Finally, we support a persistent ratings dashboard where users can submit reviews. These are saved to a local database and dynamically update their profile in real-time."*

---

## 🧪 Model Performance & Similarity Metrics

* **Vectorization Model**: TF-IDF Vectorizer (L2 Normalization, sublinear TF scaling).
* **Dimensionality**: Configured for the top `5,000` features to exclude low-frequency noise.
* **Fuzzy Matching**: Levenshtein Distance (`difflib.get_close_matches`), threshold `0.6`.
