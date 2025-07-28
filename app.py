import streamlit as st
import pandas as pd
import pickle
import os
import requests

def download_file_from_google_drive(file_id, destination):
    if not os.path.exists(destination):
        st.info(f"Downloading {destination}...")
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(url)
        
        # Check if the file looks like HTML (probably error page)
        if b'html' in response.content[:100].lower():
            st.error(f"Failed to download {destination}. Check Google Drive file permissions.")
            return

        with open(destination, 'wb') as f:
            f.write(response.content)
        st.success(f"{destination} downloaded.")

# GDrive File IDs
MOVIES_ID = "1-XBg9QTE5tAlKh7CfSj-MYiJoP-ATrmA"
SIMILARITY_ID = "1OO98hL_OVJwpTIlyh2uIFeB977lsgA43"

# Download files if not already present
download_file_from_google_drive(MOVIES_ID, "movies.pkl")
download_file_from_google_drive(SIMILARITY_ID, "similarity.pkl")

# Load pickled data
try:
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error("Error loading pickle files: " + str(e))
    st.stop()

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
