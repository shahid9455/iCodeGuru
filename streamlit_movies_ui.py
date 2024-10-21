'''
install streamlit pickle using pip install streamlit pickle
To run the file
streamlit run streamlit_movies_ui.py
'''


import streamlit as st
import pickle
import requests
import pandas as pd

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "51fa423f27a20d205d7620d6b3dd4fe5"
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url).json()
    return f"https://image.tmdb.org/t/p/w200{response.get('poster_path')}"

st.title('Movie Recommender System')
selected_movie = st.selectbox('Select a movie to get recommendations', movies['title'])
num_recommendations = st.slider('Number of recommendations', 1, 20, 5)

if st.button('Show Recommendations'):
    movie_idx = movies[movies['title'] == selected_movie].index[0]
    recommended_indices = sorted(range(len(similarity[movie_idx])), key=lambda x: similarity[movie_idx][x], reverse=True)[1:num_recommendations + 1]
    
    for i in range(0, len(recommended_indices), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(recommended_indices):
                movie_id = movies.iloc[recommended_indices[i + j]].movie_id
                col.image(fetch_poster(movie_id), width=130)
                col.write(movies.iloc[recommended_indices[i + j]].title)