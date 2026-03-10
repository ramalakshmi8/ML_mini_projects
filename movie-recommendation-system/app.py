



import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")

def fetch_poster(movie):
    url = f"http://www.omdbapi.com/?apikey=b4028a8c&t={movie}"
    data = requests.get(url).json()

    if data.get("Response") == "True":
        poster = data.get("Poster", "")

        if poster != "N/A":
            poster = poster.split("._")[0] + ".jpg"
            return poster

    # fallback poster if API fails
    return "https://via.placeholder.com/300x450?text=No+Poster"


def recommend(movie):
    movie_index = movies_list_DataFrame[movies_list_DataFrame['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list_sorted = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []
    recommendations_posters = []

    for i in movie_list_sorted:
        recommendations.append(movies_list_DataFrame.iloc[i[0]].title)
        recommendations_posters.append(fetch_poster(movies_list_DataFrame.iloc[i[0]].title))

    return recommendations,recommendations_posters


similarity = pickle.load(open("similarity.pkl", "rb"))
movies_list_DataFrame = pickle.load(open("movies.pkl", "rb"))

movies_list = movies_list_DataFrame['title'].values

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies_list
)

if st.button('Show Recommendation'):
    # recommended_movies=recommend(selected_movie_name)
    
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
