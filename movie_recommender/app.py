import streamlit as st
import pandas as pd
import pickle
import os
import recommender
from recommender import recommend, recommend_by_genre, set_api_key
import time

# Page Config
st.set_page_config(page_title="AI Movie Recommender", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("assets/styles.css")
except FileNotFoundError:
    pass

# Load models
@st.cache_resource
def load_models():
    try:
        movies_df = pickle.load(open("movies.pkl", "rb"))
        similarity = pickle.load(open("similarity.pkl", "rb"))
        return movies_df, similarity
    except FileNotFoundError:
        return None, None

movies_df, similarity = load_models()

if movies_df is None:
    st.error("Model files not found! Please run `python model_builder.py` first to generate movies.pkl and similarity.pkl.")
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='color: #a78bfa; font-family: Outfit, sans-serif;'>🎬 CineMatch</h2></div>", unsafe_allow_html=True)
    st.title("Filters & Settings")
    st.markdown("Customize your recommendation experience.")
    
    number_of_recs = st.slider("Number of Recommendations", min_value=4, max_value=12, value=4, step=4)
    
    st.markdown("---")
    st.markdown("### 🔑 TMDB API Key")
    user_api_key = st.text_input("API Key (Optional)", type="password", help="Enter your TMDB API key if you haven't added it to .env")
    if user_api_key:
        set_api_key(user_api_key)
        
    st.markdown("---")
    st.markdown("### 🍿 About")
    st.info("This AI Movie Recommendation System uses content-based filtering and Cosine Similarity to find movies tailored to your taste.")

# Hero Section
st.markdown("<h1>🎬 CineMatch Recommender</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Discover movies based on your interests, with a premium cinematic experience.</div>", unsafe_allow_html=True)

# User Input
st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>What are you in the mood for?</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    rec_mode = st.radio("Recommend by:", ("Movie Title", "Genre"), horizontal=True)
    
    if rec_mode == "Movie Title":
        movie_list = movies_df['title'].values
        selected_movie = st.selectbox(
            "Type or select a favorite movie:",
            movie_list,
            index=None,
            placeholder="Select a movie..."
        )
        recommend_clicked = st.button('Recommend Movies')
    else:
        genre_dict = {
            "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35, 
            "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751, 
            "Fantasy": 14, "History": 36, "Horror": 27, "Music": 10402, 
            "Mystery": 96, "Romance": 10749, "Science Fiction": 878, 
            "TV Movie": 10770, "Thriller": 53, "War": 10752, "Western": 37
        }
        selected_genre = st.selectbox("Select a genre:", list(genre_dict.keys()))
        recommend_clicked = st.button('Recommend by Genre')

st.markdown("<br><br>", unsafe_allow_html=True)

# Recommendation Section
if recommend_clicked:
    with st.spinner("Analyzing AI models and fetching data from TMDB..."):
        time.sleep(1) # Artificial delay for effect
        
        if rec_mode == "Movie Title":
            if not selected_movie:
                st.warning("Please select a movie first.")
                recommendations = []
            else:
                recommendations = recommend(selected_movie, movies_df, similarity, top_n=number_of_recs)
                success_msg = f"Here are {len(recommendations)} movies similar to '{selected_movie}':"
        else:
            if not recommender.TMDB_API_KEY or recommender.TMDB_API_KEY == "your_api_key_here":
                st.error("TMDB API Key is required for Genre recommendations. Please enter it in the sidebar.")
                recommendations = []
            else:
                genre_id = genre_dict[selected_genre]
                recommendations = recommend_by_genre(genre_id, top_n=number_of_recs)
                success_msg = f"Here are top {len(recommendations)} recommended movies in '{selected_genre}':"
        
        if recommendations:
            st.success(success_msg)
            
            # Responsive Grid based on number_of_recs
            cols = st.columns(4) # 4 cards per row
            
            for i, rec in enumerate(recommendations):
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="movie-card" style="margin-bottom: 20px;">
                        <img src="{rec['poster']}" class="movie-poster" alt="{rec['title']}">
                        <div class="movie-info">
                            <h3 class="movie-title" title="{rec['title']}">{rec['title']}</h3>
                            <div class="movie-meta">
                                <span>{rec['year']}</span>
                                <span class="rating">⭐ {rec['rating']}</span>
                            </div>
                            <div class="genre-tags">{rec['genres']}</div>
                            <div class="overview-text">{rec['overview']}</div>
                            <a href="{rec['trailer']}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("Sorry, we couldn't find any recommendations or there was an error with the API.")
