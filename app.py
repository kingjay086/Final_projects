import streamlit as st
import pandas as pd
import pickle
import os
import gdown

# Function to download file from Google Drive using gdown
def download_with_gdown(file_id, destination):
    if not os.path.exists(destination):
        st.info(f"Downloading {destination}...")
        url = f"https://drive.google.com/uc?id={file_id}"
        try:
            gdown.download(url, destination, quiet=False)
            st.success(f"{destination} downloaded.")
        except Exception as e:
            st.error(f"Failed to download {destination}. Error: {str(e)}")

# GDrive File IDs
MOVIES_ID = "1-XBg9QTE5tAlKh7CfSj-MYiJoP-ATrmA"
SIMILARITY_ID = "1zc_vji9oGoAzGNKFMrnyNj9r_CnfnD7y"

# Download files if not already present
download_with_gdown(MOVIES_ID, "movies.pkl")
download_with_gdown(SIMILARITY_ID, "similarity.pkl")

# Load pickled data
try:
    with open("movies.pkl", "rb") as f:
        movies = pickle.load(f)
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
except Exception as e:
    st.error("Error loading pickle files: " + str(e))
    st.stop()

# Recommender function
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
    try:
        recommendations = recommend(selected_movie)
        if recommendations:
            st.subheader("Top 5 Similar Movies:")
            for movie in recommendations:
                st.write("👉", movie)
        else:
            st.error("Movie not found in database.")
    except Exception as e:
        st.error("Recommendation failed: " + str(e))
