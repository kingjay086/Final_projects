import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# Google Drive file IDs
MOVIES_FILE_ID = "1k5pA6DLaYxtxrbgTh55JYbXmmOoWq08J"
SIMILARITY_FILE_ID = "1MT9WvIlogsvzWmmOZmmUeb0qnYEFJljz"

# Download if not already present
def download_file(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

download_file(MOVIES_FILE_ID, "movies.pkl")
download_file(SIMILARITY_FILE_ID, "similarity.pkl")

# Load model/data
with open('movies.pkl', 'rb') as f:
    movies = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# TMDB poster fetch
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<d026a6fa836620f6113427cbbb0b0ea7>>&language=en-US"
    data = requests.get(url)
    if data.status_code == 200:
        poster_path = data.json().get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/300x450?text=No+Image"

# Recommend logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters

# Streamlit UI
st.title('🎬 Movie Recommendation System')

selected_movie = st.selectbox("Choose a movie to get recommendations", movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.text(names[i])
            st.image(posters[i])
