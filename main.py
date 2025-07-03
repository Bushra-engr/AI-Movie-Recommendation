import streamlit as st
import os
import re
import time
from google import genai
from google.genai import types
from style import get_custom_css

# Page configuration
st.set_page_config(
    page_title="AI Movie/Series Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if 'recommendations_generated' not in st.session_state:
    st.session_state.recommendations_generated = False
if 'current_recommendations' not in st.session_state:
    st.session_state.current_recommendations = None

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyA2v2K4O1IL-xi21dMOOApm0QVXISYD20c"

# Initialize Gemini client
@st.cache_resource
def initialize_gemini_client():
    return genai.Client(api_key=API_KEY)

client = initialize_gemini_client()

def get_recommendations(preferences):
    """Get movie and series recommendations using Gemini API"""
    prompt = f"""You are a helpful movie assistant. Based on the user's preferences:
- Language: {preferences['lang']}
- Genre: {preferences['genre']}
- Type: {preferences['type']}
- Industry: {preferences['formula']}
- Platform: {preferences['platform']}
- Mood: {preferences['mood']}
- Year range: {preferences['year_range']}

Please provide:
- **5 movie names** under a section called `## Movies`
- **5 series names** under a section called `## Series`
- For each recommendation, provide the title followed by a brief 2-line description
- Format each recommendation as: **Title Name** - Brief description here
- Return the results in bullet format under clear headers
- Strictly no use of emojis in the response

I want to watch something in {preferences['lang']}. I'm in the mood for {preferences['genre']}. I prefer {preferences['type']} and from the {preferences['formula']} industry. I want to watch on {preferences['platform']}. My current mood is {preferences['mood']}. The movie/series should be between this year range {preferences['year_range']}. Please give me best suggestions according to my preferences."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt
        )
        return response.text if response.text else ""
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")

# Main header
st.markdown("""
<div class="main-header">
    <h1>🎬 AI Movie & Series Recommender</h1>
    <p>Discover your next favorite movie or series with AI-powered personalized recommendations</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("### 🎯 Your Preferences")
    
    # Language selection
    lang = st.selectbox(
        "🌍 Preferred Language:",
        ("Hindi", "English", "Tamil", "Telugu", "Urdu", "French", "German", "Spanish"),
        help="Select your preferred language for recommendations"
    )
    
    # Genre selection
    genre = st.multiselect(
        "🎭 Select Genres:",
        ("Horror", "Action", "Thriller", "Comedy", "Romantic", "Sci-Fi", "Family", "Drama", "Adventure", "Mystery"),
        help="Choose one or more genres you're interested in"
    )
    
    # Type selection
    type_option = st.radio(
        "📺 Content Type:",
        ("Movies", "Series", "Both"),
        help="What type of content are you looking for?"
    )
    
    # Formula/Industry selection
    formula = st.selectbox(
        "🎪 Industry:",
        ("Hollywood", "Bollywood", "Tollywood", "Korean", "Turkish", "Pakistani", "Japanese", "European"),
        help="Choose your preferred film industry"
    )
    
    # Platform selection
    platform = st.multiselect(
        "📱 Streaming Platforms:",
        ("Netflix", "Prime Video", "Disney+", "Hulu", "HBO Max", "YouTube", "Jio Cinema", "Z5", "Apple TV+"),
        help="Select your available streaming platforms"
    )
    
    # Mood selection
    mood = st.radio(
        "😊 Current Mood:",
        ("Happy", "Sad", "Neutral", "Excited", "Relaxed"),
        help="How are you feeling today?"
    )
    
    # Year range selection
    year_range = st.slider(
        "📅 Year Range:",
        min_value=1980,
        max_value=2025,
        value=(2010, 2023),
        help="Select the year range for recommendations"
    )
    
    st.markdown("---")
    
    # Submit button
    submit_button = st.button(
        "✨ Get Recommendations",
        type="primary",
        use_container_width=True
    )

# Main content area
if submit_button:
    # Validation
    if not genre:
        st.error("🚨 Please select at least one genre to get recommendations!")
    elif not platform:
        st.error("🚨 Please select at least one streaming platform!")
    else:
        # Loading state
        with st.container():
            st.markdown("""
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <div class="loading-text">🤖 AI is analyzing your preferences...</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            progress_bar.empty()
        
        # Prepare input for AI
        prompt_input = {
            "lang": lang,
            "genre": ", ".join(genre),
            "type": type_option,
            "formula": formula,
            "platform": ", ".join(platform),
            "mood": mood,
            "year_range": f"{year_range[0]}-{year_range[1]}"
        }
        
        try:
            # Get AI recommendations
            response_text = get_recommendations(prompt_input)
            
            # Store recommendations in session state
            st.session_state.current_recommendations = str(response_text)
            st.session_state.recommendations_generated = True
            
            # Clear loading state
            st.rerun()
            
        except Exception as e:
            st.markdown(f"""
            <div class="error-container">
                <h3>⚠️ Oops! Something went wrong</h3>
                <p>We encountered an error while generating recommendations: {str(e)}</p>
                <p>Please check your API key and try again.</p>
            </div>
            """, unsafe_allow_html=True)

# Display recommendations if available
if st.session_state.recommendations_generated and st.session_state.current_recommendations:
    response_text = st.session_state.current_recommendations
    
    # Results header
    st.markdown("""
    <div class="results-header">
        <h2>🎯 Your Personalized Recommendations</h2>
        <p>Based on your preferences, here are the perfect matches for you!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Parse the response
    try:
        # Split movies and series sections
        sections = re.split(r'## (Movies|Series)', str(response_text), flags=re.IGNORECASE)
        
        movies_content = ""
        series_content = ""
        
        for i in range(1, len(sections), 2):
            section_type = sections[i].lower()
            section_content = sections[i + 1] if i + 1 < len(sections) else ""
            
            if section_type == "movies":
                movies_content = section_content
            elif section_type == "series":
                series_content = section_content
        
        # Create two columns for movies and series
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="movie-card">
                <div class="card-header">
                    <div class="card-icon">🎬</div>
                    <h3 class="card-title">Movies</h3>
                </div>
            """, unsafe_allow_html=True)
            
            if movies_content.strip():
                # Extract movie recommendations
                movies = re.findall(r'[-*]\s*\*\*(.*?)\*\*\s*[-–]\s*(.*?)(?=\n|$)', movies_content, re.DOTALL)
                if not movies:
                    # Fallback pattern
                    movies = re.findall(r'[-*]\s*(.*?)(?=\n|$)', movies_content)
                    movies = [(movie.strip(), "") for movie in movies if movie.strip()]
                
                if movies:
                    for movie in movies:
                        if len(movie) == 2:
                            title, description = movie
                            st.markdown(f"""
                            <div class="recommendation-item">
                                <strong>{title.strip()}</strong>
                                <p>{description.strip()}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="recommendation-item">
                                <strong>{movie[0].strip()}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="empty-state">
                        <div class="empty-state-icon">🎬</div>
                        <h3>No Movie Recommendations</h3>
                        <p>Try adjusting your preferences for movie suggestions</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon">🎬</div>
                    <h3>No Movie Recommendations</h3>
                    <p>Try adjusting your preferences for movie suggestions</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="series-card">
                <div class="card-header">
                    <div class="card-icon">📺</div>
                    <h3 class="card-title">Series</h3>
                </div>
            """, unsafe_allow_html=True)
            
            if series_content.strip():
                # Extract series recommendations
                series = re.findall(r'[-*]\s*\*\*(.*?)\*\*\s*[-–]\s*(.*?)(?=\n|$)', series_content, re.DOTALL)
                if not series:
                    # Fallback pattern
                    series = re.findall(r'[-*]\s*(.*?)(?=\n|$)', series_content)
                    series = [(show.strip(), "") for show in series if show.strip()]
                
                if series:
                    for show in series:
                        if len(show) == 2:
                            title, description = show
                            st.markdown(f"""
                            <div class="recommendation-item">
                                <strong>{title.strip()}</strong>
                                <p>{description.strip()}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="recommendation-item">
                                <strong>{show[0].strip()}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="empty-state">
                        <div class="empty-state-icon">📺</div>
                        <h3>No Series Recommendations</h3>
                        <p>Try adjusting your preferences for series suggestions</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon">📺</div>
                    <h3>No Series Recommendations</h3>
                    <p>Try adjusting your preferences for series suggestions</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.markdown(f"""
        <div class="error-container">
            <h3>⚠️ Parsing Error</h3>
            <p>We couldn't parse the AI response properly. Here's the raw output:</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area("Raw AI Response:", response_text, height=300, disabled=True)

# Footer
if not st.session_state.recommendations_generated:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #7f8c8d;">
        <h3>👆 Set your preferences in the sidebar and get personalized recommendations!</h3>
        <p>Our AI will analyze your taste and suggest the perfect movies and series for you.</p>
    </div>
    """, unsafe_allow_html=True)

# Add a reset button at the bottom
if st.session_state.recommendations_generated:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Get New Recommendations", use_container_width=True):
            st.session_state.recommendations_generated = False
            st.session_state.current_recommendations = None
            st.rerun()
