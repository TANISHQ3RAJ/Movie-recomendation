import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import warnings

warnings.filterwarnings('ignore')

def download_and_build():
    print("Downloading TMDB 5000 datasets... This might take a minute.")
    
    # Raw URLs for TMDB 5000 dataset
    movies_url = 'https://raw.githubusercontent.com/fenago/datasets/refs/heads/main/tmdb_5000_movies.csv'
    credits_url = 'https://raw.githubusercontent.com/noahjett/Movie-Goodreads-Analysis/master/tmdb_5000_credits.csv'
    
    try:
        movies = pd.read_csv(movies_url)
        credits = pd.read_csv(credits_url)
    except Exception as e:
        print(f"Error downloading datasets: {e}")
        return

    print("Merging and processing data...")
    movies = movies.merge(credits, on='title')
    
    # Keep essential columns
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.dropna(inplace=True)

    # Helper functions to parse stringified JSON
    def convert(text):
        L = []
        try:
            for i in ast.literal_eval(text):
                L.append(i['name'])
        except Exception:
            pass
        return L

    def convert3(text):
        L = []
        counter = 0
        try:
            for i in ast.literal_eval(text):
                if counter < 3:
                    L.append(i['name'])
                    counter += 1
                else:
                    break
        except Exception:
            pass
        return L

    def fetch_director(text):
        L = []
        try:
            for i in ast.literal_eval(text):
                if i['job'] == 'Director':
                    L.append(i['name'])
                    break
        except Exception:
            pass
        return L

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert3)
    movies['crew'] = movies['crew'].apply(fetch_director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    # Remove spaces from words to create unique tags (e.g. "Science Fiction" -> "ScienceFiction")
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

    # Create the tags column
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

    new_df = movies[['movie_id', 'title', 'tags']]
    new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: " ".join(x))
    new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: x.lower())

    print("Vectorizing data and computing cosine similarity...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    
    similarity = cosine_similarity(vectors)

    print("Saving to movies.pkl and similarity.pkl...")
    with open('movies.pkl', 'wb') as f:
        pickle.dump(new_df, f)
        
    with open('similarity.pkl', 'wb') as f:
        pickle.dump(similarity, f)

    print("Successfully built the complete 5000 movies dataset! You can now restart the Streamlit app.")

if __name__ == "__main__":
    download_and_build()
