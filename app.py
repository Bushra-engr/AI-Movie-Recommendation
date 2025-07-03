import streamlit as st
from dotenv import load_dotenv
import os
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-pro",
    temperature=0.2,
    api_key=API_KEY
)

# Prompt template
movie_title_template = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful movie assistant. Based on the user's preferences (language: {lang}, genre: {genre}, type: {type}, formula: {formula}, year_range: {year_range}):
- Provide **5 movie names** under a section called `Movies`.
- Provide **5 series names** under a section called `Series`.
- Give each item a very short 2-line explanation.
- Return the results in **bullet format under clear headers**.
- Strictly no use of emojis.
"""),
    ("user", "I want to watch something in {lang}. "
             "I'm in the mood for {genre}. "
             "I prefer {type} and from the {formula} industry. "
             "I want to watch on {platform}. "
             "My current mood is {mood}. "
             "The movie/series should be between this year range {year_range}. "
             "Please give me best suggestions according to my preferences.")
])

# Streamlit UI Config
st.set_page_config(page_title="Movie/Series Recommender", layout="wide")
st.markdown("""
    <style>
    .block-container h1 {
        margin-bottom: 1rem;
        font-size: 2.8rem;
    }
    [data-testid="column"] {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    .movie-container, .series-container {
        background-color: #f9f9f9;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.4rem 1.2rem;
    }
    section[data-testid="stSidebar"] {
        background-color: #111;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.title("🎥 AI Movie/Series Recommender")

# Sidebar Input
lang = st.sidebar.selectbox("Choose your preferred language:", 
    ("Hindi", "English", "Tamil", "Telugu", "Urdu", "French", "German", "Spanish"))
genre = st.sidebar.multiselect("Select Genre:", 
    ("Horror", "Action", "Thriller", "Comedy", "Romantic", "Sci-Fi", "Family"))
type = st.sidebar.radio("Select Type:", ("Movies", "Series", "Both"))
formula = st.sidebar.selectbox("Select Formula Type:", 
    ("Hollywood", "Bollywood", "Tollywood", "Korean", "Turkish", "Pakistani"))
platform = st.sidebar.multiselect("Select Platform:", 
    ("YouTube", "Netflix", "Prime Video", "Disney +", "Jio Cinema", "Z5"))
mood = st.sidebar.radio("Your Mood:", ("Happy", "Sad", "Neutral"))
year_range = st.sidebar.slider("Select Year Range:", 1980, 2025, (2010, 2023))

submit = st.sidebar.button("Submit", type="primary")

# Submit Handling
if submit:
    st.subheader("🎯 Recommended Movies & Series")

    prompt_input = {
        "lang": lang,
        "genre": genre,
        "type": type,
        "formula": formula,
        "platform": platform,
        "mood": mood,
        "year_range": year_range
    }

    user_movie_prompt = movie_title_template.invoke(prompt_input)
    response = llm.invoke(user_movie_prompt)
    response_text = response.content

    match = re.split(r"(?i)###?\s*Series", response_text)
    if len(match) == 2:
        movies_section, series_section = match
        movies = re.findall(r"\*+\s+(.*)", movies_section)
        series = re.findall(r"\*+\s+(.*)", series_section)

        col1, col2 = st.columns(2, gap="small")

        with col1:
            with st.container():
                st.markdown("<div class='movie-container'>", unsafe_allow_html=True)
                st.subheader("🎬 Movies")
                if movies:
                    for movie in movies:
                        st.markdown(f"- {movie}")
                else:
                    st.info("No movie results found.")
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            with st.container():
                st.markdown("<div class='series-container'>", unsafe_allow_html=True)
                st.subheader("📺 Series")
                if series:
                    for show in series:
                        st.markdown(f"- {show}")
                else:
                    st.info("No series results found.")
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Couldn't parse AI output. Showing raw response:")
        st.text_area("Debug Output:", response_text, height=300)
