import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load CSVs with safe file paths (adjust if needed)
movies = pd.read_csv(r"C:\Users\jay30\OneDrive\Documents\myprojects\python\tmdb_5000_movies.csv")
credits = pd.read_csv(r"C:\Users\jay30\OneDrive\Documents\myprojects\python\tmdb_5000_credits.csv")

# Merge on 'title'
movies = movies.merge(credits, on='title')

# Keep only relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Drop any missing overviews
movies.dropna(inplace=True)

# Function to extract 'name' from list-like strings
def extract_names(obj):
    try:
        return [i['name'] for i in ast.literal_eval(obj)]
    except:
        return []

# Top 3 cast members
def extract_top_cast(obj):
    try:
        return [i['name'] for i in ast.literal_eval(obj)[:3]]
    except:
        return []

# Director only from crew
def extract_director(obj):
    try:
        return [i['name'] for i in ast.literal_eval(obj) if i['job'] == 'Director']
    except:
        return []

# Apply cleaning
movies['genres'] = movies['genres'].apply(extract_names)
movies['keywords'] = movies['keywords'].apply(extract_names)
movies['cast'] = movies['cast'].apply(extract_top_cast)
movies['crew'] = movies['crew'].apply(extract_director)

# Remove spaces and lowercase
def clean_list(lst):
    return [i.replace(" ", "").lower() for i in lst]

for col in ['genres', 'keywords', 'cast', 'crew']:
    movies[col] = movies[col].apply(clean_list)

# Combine all into a single string column for NLP
movies['overview'] = movies['overview'].apply(lambda x: x.lower().split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

# Final dataset
final = movies[['movie_id', 'title', 'tags']]

# Vectorize tags
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(final['tags']).toarray()

# Compute cosine similarity
similarity = cosine_similarity(vectors)

# Save for Streamlit app
pickle.dump(final, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("✅ Model training complete and files saved as movies.pkl & similarity.pkl")
