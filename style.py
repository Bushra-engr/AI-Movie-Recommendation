"""
Custom CSS styles for the Movie/Series Recommender application
"""

def get_custom_css():
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    .css-1d391kg .css-1outpf7 {
        background-color: transparent;
        color: white;
    }
    
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stMultiSelect label,
    .css-1d391kg .stRadio label,
    .css-1d391kg .stSlider label {
        color: #ecf0f1 !important;
        font-weight: 500;
        font-size: 1rem;
    }
    
    .css-1d391kg .stSelectbox > div > div,
    .css-1d391kg .stMultiSelect > div > div {
        background-color: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        color: white;
    }
    
    .css-1d391kg .stRadio > div {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .css-1d391kg .stSlider > div > div {
        background-color: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Submit Button Enhancement */
    .css-1d391kg .stButton > button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(231,76,60,0.4);
    }
    
    .css-1d391kg .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(231,76,60,0.6);
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        margin: 2rem 0;
    }
    
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #FF4B4B;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        margin-left: 1rem;
        font-size: 1.2rem;
        color: #666;
        font-weight: 500;
    }
    
    /* Results Container */
    .results-header {
        text-align: center;
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 8px 25px rgba(116,185,255,0.3);
    }
    
    .results-header h2 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .results-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Movie and Series Cards */
    .movie-card, .series-card {
        background-color:skyblue;
        border-radius: 20px;
        padding: 2rem;
        color:#111;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .movie-card:hover, .series-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
    }
    
    .series-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #a8e6cf, #81c784);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f1f3f4;
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-right: 1rem;
    }
    
    .card-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }
    
    /* Recommendation Items */
    .recommendation-item {
        background: rgba(255,255,255,0.8);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #FF4B4B;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .recommendation-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .recommendation-item strong {
        color: #2c3e50;
        font-size: 1.1rem;
    }
    
    .recommendation-item p {
        color: #7f8c8d;
        margin: 0.5rem 0 0 0;
        line-height: 1.4;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        border-radius: 20px;
        margin: 1rem 0;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.7;
    }
    
    .empty-state h3 {
        color: #2d3436;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .empty-state p {
        color: #636e72;
        margin-bottom: 0;
    }
    
    /* Error State */
    .error-container {
        background: linear-gradient(135deg, #fab1a0 0%, #e17055 100%);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .error-container h3 {
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .error-container textarea {
        background: rgba(255,255,255,0.1);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .card-title {
            font-size: 1.5rem;
        }
        
        .movie-card, .series-card {
            padding: 1.5rem;
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """