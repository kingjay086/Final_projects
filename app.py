import streamlit as st
import pickle
import pandas as pd

# Load the preprocessed data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommend function
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = list(enumerate(similarity[movie_index]))
        movie_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
        return [movies.iloc[i[0]].title for i in movie_list]
    except:
        return []

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
