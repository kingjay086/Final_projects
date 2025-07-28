import streamlit as st
import pandas as pd
import pickle
import os
import requests
import gdown

def download_file_from_google_drive(url, destination):
    if not os.path.exists(destination):
        st.info(f"Downloading {destination}...")
        r = requests.get(url, allow_redirects=True)
        open(destination, 'wb').write(r.content)
        st.success(f"{destination} downloaded.")

#  GDrive links
MOVIES_URL = "https://drive.google.com/uc?export=download&id=1k5pA6DLaYxtxrbgTh55JYbXmmOoWq08J"
SIMILARITY_URL = "https://drive.google.com/uc?export=download&id=1k5pA6DLaYxtxrbgTh55JYbXmmOoWq08J"

download_file_from_google_drive(MOVIES_URL, "movies.pkl")
download_file_from_google_drive(SIMILARITY_URL, "similarity.pkl")

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Search or select a movie:", movies['title'].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    if recommendations:
        st.subheader("Top 5 Similar Movies:")
        for movie in recommendations:
            st.write(">>", movie)
    else:
        st.error("Movie not found in database.")
