import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.request
import io

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies ['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies =[]
    recommended_movies_posters =[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# -------- Load data from GitHub --------
similarity_url = "https://github.com/yapa-proga/movie_recom/releases/download/v1.1/similarity.pkl"
response_sim = requests.get(similarity_url)
similarity = pickle.load(io.BytesIO(response_sim.content))

movies_url = "https://github.com/yapa-proga/movie_recom/releases/download/v1.1/movies_dict.pkl"
response_movies = requests.get(movies_url)
movies_dict ="https://github.com/yapa-proga/movie_recom/raw/refs/heads/main/movies_dict.pkl"
response_movie_dict = requests.get(movies_dict)
#movies_dict = pickle.load(io.BytesIO(response.content))
#response_movies = urllib.request.urlopen(movies_url)
#movies_dict = pickle.load(io.BytesIO(response_movies.read()))
movies = pd.DataFrame(movies_dict)

#--------------UI----------

st.set_page_config(
    page_title="Movie Recommender",  # Title that appears in the browser tab
    page_icon="🎬",  # App icon (emoji)
    layout="wide",  # Layout style, 'wide' gives more space for content
    initial_sidebar_state="collapsed",  # Sidebar state
)

# Add custom styling using CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;  /* Dark background color for the entire app */
    }
    .stButton>button {
        background-color: #00ccff;  /* Button color */
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0099cc;  /* Hover effect */
        transition: 0.3s;
    }
    .stTitle, .stSubheader, .stText {
        color: white;  /* Text color */
    }
    .stSelectbox select, .stTextInput input {
        color: black;
    }
    .css-1v0mbdj {
        font-family: 'Courier New', Courier, monospace;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.markdown("<h1 style='text-align: center; color: white;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Get Similar Movies with Just One Click</h3>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Movie recommender UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h4 style='color: white;'>Recommended Movies:</h4>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

# Footer section
st.markdown("""
    <hr style="border:1px solid #555;">
    <div style="text-align:center; padding: 10px; font-size: 14px; color: #aaa;">
        Made with ❤️ with help of some brain 🧠<br>
        © 2025 Movie Recommender | Built by Yashu
    </div>
""", unsafe_allow_html=True)
