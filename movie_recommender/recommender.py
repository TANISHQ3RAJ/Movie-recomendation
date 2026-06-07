import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def set_api_key(key):
    global TMDB_API_KEY
    TMDB_API_KEY = key

def fetch_poster(movie_id):
    if not TMDB_API_KEY or TMDB_API_KEY == "your_api_key_here":
        return "https://placehold.co/500x750/1a1a2e/7c3aed.png?text=No+API+Key"
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://placehold.co/500x750/1a1a2e/7c3aed.png?text=No+Poster"
    except Exception as e:
        return "https://placehold.co/500x750/1a1a2e/7c3aed.png?text=Error"

def fetch_movie_details(movie_id):
    if not TMDB_API_KEY or TMDB_API_KEY == "your_api_key_here":
        return {"rating": "N/A", "year": "N/A", "genres": "API Key Req", "overview": "Please add TMDB API key to .env file to see details."}
        
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        rating = data.get('vote_average', "N/A")
        if isinstance(rating, float): rating = round(rating, 1)
        year = data.get('release_date', "N/A")[:4] if data.get('release_date') else "N/A"
        genres = ", ".join([g['name'] for g in data.get('genres', [])])[:40]
        if not genres: genres = "Unknown"
        overview = data.get('overview', "No overview available.")
        if len(overview) > 120: overview = overview[:117] + "..."
        return {"rating": rating, "year": year, "genres": genres, "overview": overview}
    except Exception:
        return {"rating": "N/A", "year": "N/A", "genres": "Unknown", "overview": "Error fetching details"}

def get_trailer_url(movie_id, title=""):
    fallback_url = f"https://www.youtube.com/results?search_query={title.replace(' ', '+')}+trailer" if title else "#"
    if not TMDB_API_KEY or TMDB_API_KEY == "your_api_key_here":
        return fallback_url
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        for res in data.get('results', []):
            if res['type'] == 'Trailer' and res['site'] == 'YouTube':
                return f"https://www.youtube.com/watch?v={res['key']}"
        return fallback_url
    except Exception:
        return fallback_url

def recommend(movie, movies_df, similarity, top_n=5):
    try:
        # Find index of movie
        movie_index = movies_df[movies_df['title'].str.lower() == movie.lower()].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:top_n+1]
        
        recommended_movies = []
        for i in movies_list:
            movie_id = movies_df.iloc[i[0]].movie_id
            title = movies_df.iloc[i[0]].title
            poster = fetch_poster(movie_id)
            details = fetch_movie_details(movie_id)
            trailer = get_trailer_url(movie_id, title)
            
            recommended_movies.append({
                "title": title,
                "poster": poster,
                "rating": details["rating"],
                "year": details["year"],
                "genres": details["genres"],
                "overview": details["overview"],
                "trailer": trailer
            })
            
        return recommended_movies
    except Exception as e:
        print(f"Error in recommend: {e}")
        return []

def recommend_by_genre(genre_id, top_n=5):
    if not TMDB_API_KEY or TMDB_API_KEY == "your_api_key_here":
        return []
    
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&language=en-US&sort_by=popularity.desc"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        recommended_movies = []
        for item in data.get('results', [])[:top_n]:
            movie_id = item['id']
            title = item['title']
            
            poster = "https://image.tmdb.org/t/p/w500/" + item['poster_path'] if item.get('poster_path') else "https://placehold.co/500x750/1a1a2e/7c3aed.png?text=No+Poster"
            
            rating = item.get('vote_average', "N/A")
            if isinstance(rating, float): rating = round(rating, 1)
            year = item.get('release_date', "N/A")[:4] if item.get('release_date') else "N/A"
            overview = item.get('overview', "No overview available.")
            if len(overview) > 120: overview = overview[:117] + "..."
            
            trailer = get_trailer_url(movie_id, title)
            details = fetch_movie_details(movie_id)
            
            recommended_movies.append({
                "title": title,
                "poster": poster,
                "rating": rating,
                "year": year,
                "genres": details.get("genres", "Unknown"),
                "overview": overview,
                "trailer": trailer
            })
            
        return recommended_movies
    except Exception as e:
        print(f"Error in recommend_by_genre: {e}")
        return []
