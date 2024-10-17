import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        )
        data = response.json()
        return data['poster_path']
    except Exception as e:
        return ""

# Function to recommend movies based on similarity
def recommend(movie):
    try:
        # Get the index of the selected movie
        movies_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movies_index]

        # Get top 5 similar movies
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommend_movies = []
        recommend_movies_poster = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            poster_path = fetch_poster(movie_id)
            recommend_movies.append(movies.iloc[i[0]].title)
            recommend_movies_poster.append(poster_path)

        return recommend_movies, recommend_movies_poster
    except Exception as e:
        st.error(f"Error during recommendation: {e}")
        return [], []

# Check if the necessary files exist
if os.path.exists('movies_dict.pkl') and os.path.exists('similarity.pkl'):
    # Load movies and similarity data
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
    # Streamlit app title
    st.title('Movies Recommender System')

    # Dropdown for selecting a movie
    selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

    # Button to trigger recommendation
    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)

        # Display recommendations with posters
        if names:
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.text(names[0])
                if posters[0]:
                    st.image("https://image.tmdb.org/t/p/w200" + posters[0])
                else:
                    st.text("Poster not available")

            with col2:
                st.text(names[1])
                if posters[1]:
                    st.image("https://image.tmdb.org/t/p/w200" + posters[1])
                else:
                    st.text("Poster not available")

            with col3:
                st.text(names[2])
                if posters[2]:
                    st.image("https://image.tmdb.org/t/p/w200" + posters[2])
                else:
                    st.text("Poster not available")

            with col4:
                st.text(names[3])
                if posters[3]:
                    st.image("https://image.tmdb.org/t/p/w200" + posters[3])
                else:
                    st.text("Poster not available")

            with col5:
                st.text(names[4])
                if posters[4]:
                    st.image("https://image.tmdb.org/t/p/w200" + posters[4])
                else:
                    st.text("Poster not available")
        else:
            st.warning("No recommendations available.")
else:
    st.error("Required files ('movies_dict.pkl' or 'similarity.pkl') not found. Please upload the necessary files.")
