import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_KEY = "ce27b487d5d5f513d48e893f7468212b"

# Create a session with automatic retries
session = requests.Session()
retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))


def fetch_poster(movie_id):
    try:
        response = session.get(
            'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, API_KEY),
            timeout=15
        )
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        print(f"Poster fetch failed for movie {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0]); st.image(posters[0])
    with col2:
        st.text(names[1]); st.image(posters[1])
    with col3:
        st.text(names[2]); st.image(posters[2])
    with col4:
        st.text(names[3]); st.image(posters[3])
    with col5:
        st.text(names[4]); st.image(posters[4])
