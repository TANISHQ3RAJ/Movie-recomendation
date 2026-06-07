# 🎬 AI Movie Recommendation System

**Live Demo:** [https://movie-recomendation-hd.streamlit.app/](https://movie-recomendation-hd.streamlit.app/)

A modern, visually stunning, fully functional AI-powered Movie Recommendation Web App built with Streamlit and Python. It uses a content-based filtering approach (Cosine Similarity) and fetches dynamic movie data and posters from the TMDB API.

## Features
- **Netflix-Inspired UI**: Dark theme with glassmorphism movie cards and hover effects.
- **Content-Based Filtering**: Recommends movies based on genres, keywords, cast, and crew.
- **TMDB API Integration**: Dynamically fetches posters, ratings, overview, and trailer links.
- **Fully Responsive**: Adapts to various screen sizes.
- **Customizable**: Sidebar to adjust the number of recommendations.

---

## 🚀 Setup Instructions

### 1. Clone/Download the Project
Ensure you are in the `movie_recommender` directory.

### 2. Create a Virtual Environment (Optional but recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate the AI Models (If not already present)
We have included a mock script to generate a small dataset of 10+ movies to get you started immediately:
```bash
python model_builder.py
```
*(This will generate `movies.pkl` and `similarity.pkl`)*

> **Note**: To use the full TMDB 5000 dataset, you will need to download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from Kaggle, and update `model_builder.py` to process those CSV files into the `.pkl` files.

### 5. TMDB API Setup
To fetch movie posters and details, you need a TMDB API key.
1. Go to [TMDB](https://www.themoviedb.org/) and create an account.
2. Go to your account settings -> API -> Request an API Key.
3. Open the `.env` file in the root of this project and paste your key:
```env
TMDB_API_KEY=your_actual_api_key_here
```

### 6. Run the App
```bash
streamlit run app.py
```

---

## 🛠️ How the Recommendation Works
1. **Data**: The system relies on a dataset of movies with their tags (genres, overview, keywords, cast, crew).
2. **Vectorization**: We use `CountVectorizer` from `scikit-learn` to convert text data into vectors.
3. **Similarity**: We calculate the `cosine_similarity` between all movies based on these vectors.
4. **Recommendation**: When a user selects a movie, we find the index of that movie, look up its similarity scores, sort them, and fetch the top N most similar movies.

## 🚀 Deployment Guide
This project is deployment-ready for platforms like **Streamlit Cloud**, **Render**, or **Hugging Face Spaces**.

**For Streamlit Cloud:**
1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
3. Select the repository and set the main file path to `app.py`.
4. **Important**: Go to "Advanced Settings" during setup and add your `TMDB_API_KEY` to the Secrets section so the app can fetch posters in production.
5. Click **Deploy!**

---
Made with ❤️ using Streamlit & Python.
