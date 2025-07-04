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

If type is "Movies":
- Provide **5 movie names** under a section called `Movies`.
- Do NOT provide any series.

If type is "Series":
- Provide **5 series names** under a section called `Series`.
- Do NOT provide any movies.

If type is "Both":
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

# Enhanced CSS for better UI with responsive design
st.markdown("""
    <style>
    /* Base container styling with responsive max-width */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1000px;
        margin: 0 auto;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Header styling - responsive */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .main-title h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
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
    
    /* Button styling - responsive */
    .stButton > button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(231,76,60,0.3);
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(231,76,60,0.4);
    }
    
    /* Results section styling */
    .results-section {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(116,185,255,0.3);
    }
    
    /* Responsive grid layout for recommendations */
    .recommendations-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    /* Movie and Series cards - responsive */
    .movie-container, .series-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        width:37vw;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #00d2ff;
        height: fit-content;
        margin-bottom:1.5rem; "
    }
    
    .movie-container h2, .series-container h2 {
        color: white;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 0.8rem;
        text-align: center;
        border-bottom: 2px solid rgba(255,255,255,0.2);
        padding-bottom: 0.4rem;
    }
    
    .movie-container ul, .series-container ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .movie-container li, .series-container li {
        margin-bottom: 0.8rem;
        padding: 0.3rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        line-height: 1.4;
        font-size: 0.9rem;
    }
    
    .movie-container li:last-child, .series-container li:last-child {
        border-bottom: none;
    }
    
    /* Loading animation */
    .loading {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 300;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .loading h2 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
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
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .error-box h3 {
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    /* Info message styling */
    .info-message {
        text-align: center;
        padding: 3rem 2rem;
        color: #6c757d;
        background: rgba(108, 117, 125, 0.1);
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .info-message h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: #495057;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .main-title h1 {
            font-size: 2rem;
        }
        
        .main-title p {
            font-size: 1rem;
        }
        
        .main-title {
            padding: 1.5rem 1rem;
        }
        
        .recommendations-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .movie-container, .series-container {
            padding: 1rem;
            min-height: auto;
        }
        
        .movie-container h2, .series-container h2 {
            font-size: 1.3rem;
        }
        
        .loading {
            padding: 2rem 1rem;
        }
        
        .error-box {
            padding: 1.5rem;
        }
        
        .info-message {
            padding: 2rem 1rem;
        }
    }
    
    /* Small mobile devices */
    @media (max-width: 480px) {
        .main-title h1 {
            font-size: 1.8rem;
        }
        
        .main-title {
            padding: 1rem;
        }
        
        .movie-container, .series-container {
            padding: 0.8rem;
        }
        
        .movie-container h2, .series-container h2 {
            font-size: 1.2rem;
        }
        
        .movie-container li, .series-container li {
            font-size: 0.9rem;
        }
    }
    
    /* Large screens */
    @media (min-width: 1200px) {
        .main .block-container {
            max-width: 1200px;
        }
        
        .recommendations-grid {
            gap: 3rem;
        }
        
        .movie-container, .series-container {
            padding: 2rem;
        }
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
    ("YouTube", "Netflix", "Prime Video", "Disney+", "Jio Cinema", "Z5", "Hulu", "HBO Max","AppleTv"))

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
                <h2>🤖 AI is analyzing your preferences...</h2>
                <p>Please wait while we generate personalized recommendations for you.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Prepare prompt input
        prompt_input = {
            "lang": lang,
            "genre": ", ".join(genre),
            "type": type,
            "formula": formula,
            "platform": ", ".join(platform),
            "mood": mood,
            "year_range": f"{year_range[0]}-{year_range[1]}"
        }

        try:
            user_movie_prompt = movie_title_template.invoke(prompt_input)
            response = llm.invoke(user_movie_prompt)
            response_text = response.content

            # Parse the response
            if isinstance(response_text, str):
                # Initialize empty lists
                movies = []
                series = []
                
                # Split by Series section if it exists
                series_split = re.split(r"(?i)###?\s*Series", response_text)
                if len(series_split) == 2:
                    movies_section, series_section = series_split
                    movies = re.findall(r"[-*•]\s+(.*?)(?=\n[-*•]|\n\n|$)", movies_section, re.DOTALL)
                    series = re.findall(r"[-*•]\s+(.*?)(?=\n[-*•]|\n\n|$)", series_section, re.DOTALL)
                else:
                    # Check if it's only movies or only series
                    if "Movies" in response_text and "Series" not in response_text:
                        # Only movies
                        movies = re.findall(r"[-*•]\s+(.*?)(?=\n[-*•]|\n\n|$)", response_text, re.DOTALL)
                    elif "Series" in response_text and "Movies" not in response_text:
                        # Only series
                        series = re.findall(r"[-*•]\s+(.*?)(?=\n[-*•]|\n\n|$)", response_text, re.DOTALL)
                    else:
                        # Try to parse both from the entire text
                        movies = re.findall(r"[-*•]\s+(.*?)(?=\n[-*•]|\n\n|$)", response_text, re.DOTALL)
                
                # Display results based on user selection
                if type == "Both":
                    # Show both movies and series
                    st.markdown('<div class="recommendations-grid">', unsafe_allow_html=True)
                    col1, col2 = st.columns(2, gap="medium")

                    with col1:
                        st.markdown("""
                        <div class="movie-container">
                            <h2>🎬 Movies</h2>
                            <ul>
                        """, unsafe_allow_html=True)
                        
                        if movies:
                            for movie in movies[:5]:
                                clean_movie = movie.strip().replace('\n', ' ')
                                st.markdown(f"<li>{clean_movie}</li>", unsafe_allow_html=True)
                        else:
                            st.markdown("<li>No movie results found for your preferences.</li>", unsafe_allow_html=True)
                        
                        st.markdown("</ul></div>", unsafe_allow_html=True)

                    with col2:
                        st.markdown("""
                        <div class="series-container">
                            <h2>📺 Series</h2>
                            <ul>
                        """, unsafe_allow_html=True)
                        
                        if series:
                            for show in series[:5]:
                                clean_show = show.strip().replace('\n', ' ')
                                st.markdown(f"<li>{clean_show}</li>", unsafe_allow_html=True)
                        else:
                            st.markdown("<li>No series results found for your preferences.</li>", unsafe_allow_html=True)
                        
                        st.markdown("</ul></div>", unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                elif type == "Movies":
                    # Show only movies - centered
                    st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
                    st.markdown("""
                    <div class="movie-container" style="max-width: 600px;">
                        <h3>🎬 Movies</h3>
                        <ul>
                    """, unsafe_allow_html=True)
                    
                    if movies:
                        for movie in movies[:5]:
                            clean_movie = movie.strip().replace('\n', ' ')
                            st.markdown(f"<li>{clean_movie}</li>", unsafe_allow_html=True)
                    else:
                        st.markdown("<li>No movie results found for your preferences.</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div></div>", unsafe_allow_html=True)
                
                elif type == "Series":
                    # Show only series - centered
                    st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
                    st.markdown("""
                    <div class="series-container" style="max-width: 600px;">
                        <h3>📺 Series</h3>
                        <ul>
                    """, unsafe_allow_html=True)
                    
                    if series:
                        for show in series[:5]:
                            clean_show = show.strip().replace('\n', ' ')
                            st.markdown(f"<li>{clean_show}</li>", unsafe_allow_html=True)
                    else:
                        st.markdown("<li>No series results found for your preferences.</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div></div>", unsafe_allow_html=True)
                
            else:
                # Handle non-string response
                st.markdown("""
                <div class="error-box">
                    <h3>⚠️ Invalid response format</h3>
                    <p>The AI returned an unexpected response format.</p>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"""
            <div class="error-box">
                <h3>⚠️ Error generating recommendations</h3>
                <p>Something went wrong: {str(e)}</p>
                <p>Please check your API key and try again.</p>
            </div>
            """, unsafe_allow_html=True)

# Footer - show when no submission
if not submit:
    st.markdown("""
    <div class="info-message">
        <h3>👈 Fill in your preferences in the sidebar to get started!</h3>
        <p>Select your genres and platforms to receive personalized movie and series recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
