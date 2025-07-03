import streamlit as st
from dotenv import load_dotenv
import os
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyA2v2K4O1IL-xi21dMOOApm0QVXISYD20c"

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
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

# Enhanced CSS for better UI
st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding:1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-title h1 {
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
        font-weight: 700;
    }
    
    .main-title p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stMultiSelect label,
    .css-1d391kg .stRadio label,
    .css-1d391kg .stSlider label {
        color: white !important;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(231,76,60,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(231,76,60,0.4);
    }
    
    /* Results container */
    .results-section {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(116,185,255,0.3);
    }
    
    /* Movie and Series cards */
    .movie-container, .series-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #FF4B4B;
    }
    
    .movie-container h3, .series-container h3 {
        color: #111;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .movie-container li, .series-container li {
        margin-bottom: 0.2renm
        color: #111;
        line-height: 1.4;
    }
    
    /* Loading animation */
    .loading {
        text-align: center;
        padding: 2rem;
        background: #111;
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    /* Required field indicator */
    .required {
        color: #e74c3c;
        font-weight: bold;
    }
    
    /* Error styling */
    .error-box {
        background: linear-gradient(135deg, #fab1a0 0%, #e17055 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("""
<div class="main-title">
    <h1>🎥 AI Movie/Series Recommender</h1>
    <p>Get personalized recommendations based on your preferences</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Input with validation
st.sidebar.markdown("### 🎯 Set Your Preferences")
st.sidebar.markdown('<p class="required">* Required fields</p>', unsafe_allow_html=True)

lang = st.sidebar.selectbox("Choose your preferred language:", 
    ("Hindi", "English", "Tamil", "Telugu", "Urdu", "French", "German", "Spanish"))

genre = st.sidebar.multiselect("Select Genre: *", 
    ("Horror", "Action", "Thriller", "Comedy", "Romantic", "Sci-Fi", "Family", "Drama", "Adventure"))

type = st.sidebar.radio("Select Type:", ("Movies", "Series", "Both"))

formula = st.sidebar.selectbox("Select Formula Type:", 
    ("Hollywood", "Bollywood", "Tollywood", "Korean", "Turkish", "Pakistani"))

platform = st.sidebar.multiselect("Select Platform: *", 
    ("YouTube", "Netflix", "Prime Video", "Disney+", "Jio Cinema", "Z5", "Hulu", "HBO Max"))

mood = st.sidebar.radio("Your Mood:", ("Happy", "Sad", "Neutral", "Excited", "Relaxed"))

year_range = st.sidebar.slider("Select Year Range:", 1980, 2025, (2010, 2023))

submit = st.sidebar.button("🎬 Get Recommendations", type="primary")

# Validation and Submit Handling
if submit:
    # Check required fields
    missing_fields = []
    if not genre:
        missing_fields.append("Genre")
    if not platform:
        missing_fields.append("Platform")
    
    if missing_fields:
        st.markdown(f"""
        <div class="error-box">
            <h3>⚠️ Missing Required Information</h3>
            <p>Please fill in the following required fields: <strong>{', '.join(missing_fields)}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show loading
        with st.container():
            st.markdown("""
            <div class="loading">
                <h3>🤖 AI is analyzing your preferences...</h3>
                <p>Please wait while we generate personalized recommendations for you.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show results header
        st.markdown("""
        <div class="results-section">
            <h2>🎯 Your Personalized Recommendations</h2>
            <p>Based on your preferences, here are the perfect matches!</p>
        </div>
        """, unsafe_allow_html=True)

        prompt_input = {
            "lang": lang,
            "genre": genre,
            "type": type,
            "formula": formula,
            "platform": platform,
            "mood": mood,
            "year_range": year_range
        }

        try:
            user_movie_prompt = movie_title_template.invoke(prompt_input)
            response = llm.invoke(user_movie_prompt)
            response_text = response.content

            match = re.split(r"(?i)###?\s*Series", response_text)
            if len(match) == 2:
                movies_section, series_section = match
                movies = re.findall(r"\*+\s+(.*)", movies_section)
                series = re.findall(r"\*+\s+(.*)", series_section)

                col1, col2 = st.columns(2, gap="medium")

                with col1:
                    st.markdown("""
                    <div class="movie-container">
                        <h3>🎬 Movies</h3>
                    """, unsafe_allow_html=True)
                    
                    if movies:
                        for movie in movies:
                            st.markdown(f"• {movie}")
                    else:
                        st.info("No movie results found for your preferences.")
                    
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("""
                    <div class="series-container">
                        <h3>📺 Series</h3>
                    """, unsafe_allow_html=True)
                    
                    if series:
                        for show in series:
                            st.markdown(f"• {show}")
                    else:
                        st.info("No series results found for your preferences.")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-box">
                    <h3>⚠️ Could not parse recommendations</h3>
                    <p>Here's the raw response from AI:</p>
                </div>
                """, unsafe_allow_html=True)
                st.text_area("Debug Output:", response_text, height=300)

        except Exception as e:
            st.markdown(f"""
            <div class="error-box">
                <h3>⚠️ Error generating recommendations</h3>
                <p>Something went wrong: {str(e)}</p>
                <p>Please check your API key and try again.</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
if not submit:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #6c757d;">
        <h3>👈 Fill in your preferences in the sidebar to get started!</h3>
        <p>Select your genres and platforms to receive personalized movie and series recommendations.</p>
    </div>
    """, unsafe_allow_html=True)