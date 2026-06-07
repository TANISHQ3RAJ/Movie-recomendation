import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

def create_mock_dataset():
    """Creates a mock dataset to test the app out-of-the-box."""
    print("Generating mock dataset...")
    
    # Real TMDB IDs to ensure API fetching works when they add a key
    data = [
        {"movie_id": 19995, "title": "Avatar", "tags": "action adventure fantasy science fiction"},
        {"movie_id": 299536, "title": "Avengers: Infinity War", "tags": "action adventure science fiction superhero"},
        {"movie_id": 155, "title": "The Dark Knight", "tags": "action crime drama thriller batman superhero"},
        {"movie_id": 27205, "title": "Inception", "tags": "action thriller science fiction mystery mind-bending"},
        {"movie_id": 157336, "title": "Interstellar", "tags": "adventure drama science fiction space time-travel"},
        {"movie_id": 550, "title": "Fight Club", "tags": "drama psychology underground fighting"},
        {"movie_id": 680, "title": "Pulp Fiction", "tags": "crime drama thriller mafia classic"},
        {"movie_id": 13, "title": "Forrest Gump", "tags": "comedy drama romance classic touching"},
        {"movie_id": 603, "title": "The Matrix", "tags": "action science fiction cyberpunk hacker"},
        {"movie_id": 120, "title": "The Lord of the Rings: The Fellowship of the Ring", "tags": "adventure fantasy action epic ring"},
        {"movie_id": 11, "title": "Star Wars", "tags": "adventure action science fiction space classic"},
        {"movie_id": 118340, "title": "Guardians of the Galaxy", "tags": "action science fiction adventure space marvel superhero"},
        {"movie_id": 76341, "title": "Mad Max: Fury Road", "tags": "action adventure science fiction post-apocalyptic"},
    ]
    
    movies = pd.DataFrame(data)
    
    # Vectorization
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    
    # Cosine Similarity
    similarity = cosine_similarity(vectors)
    
    # Save to pickle
    pickle.dump(movies, open('movies.pkl', 'wb'))
    pickle.dump(similarity, open('similarity.pkl', 'wb'))
    
    print("Successfully generated movies.pkl and similarity.pkl!")
    print("You can now run the app using `streamlit run app.py`")

if __name__ == "__main__":
    create_mock_dataset()
