import streamlit as st
import pickle
import pandas as pd
import requests
import io

# --- Utility Functions ---
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')

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

# --- Function to Load Pickle from URL ---
def load_pickle_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pickle.load(io.BytesIO(response.content))
    except Exception as e:
        st.error(f"Failed to load pickle file from {url}\nError: {e}")
        st.stop()

# --- Load Your Data ---
similarity_url = "https://github.com/yapa-proga/movie_recom/releases/download/v1.1/similarity.pkl"
movies_url = "https://github.com/yapa-proga/movie_recom/releases/download/v1.2/movies_dict.pkl"

similarity = load_pickle_from_url(similarity_url)
movies_dict = load_pickle_from_url(movies_url)
movies = pd.DataFrame(movies_dict)

# --- Streamlit UI ---
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS
st.markdown(
    """
    <style>
    .stApp { background-color: #0E1117; }
    .stButton>button {
        background-color: #00ccff; color: white; border-radius: 8px;
        padding: 0.5em 1em; font-size: 16px;
    }
    .stButton>button:hover { background-color: #0099cc; transition: 0.3s; }
    .stTitle, .stSubheader, .stText { color: white; }
    .stSelectbox select, .stTextInput input { color: black; }
    .css-1v0mbdj { font-family: 'Courier New', Courier, monospace; font-size: 18px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: white;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Get Similar Movies with Just One Click</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

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

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

st.markdown("""
    <hr style="border:1px solid #555;">
    <div style="text-align:center; padding: 10px; font-size: 14px; color: #aaa;">
        Made with ❤️ with help of some brain 🧠<br>
        © 2025 Movie Recommender | Built by Yashu
    </div>
""", unsafe_allow_html=True)
