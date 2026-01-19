"""
NewGrader Custom Styling Module - Tab-based Navigation Version
Professional UI styling with Navy Blue & White theme (No Sidebar)
"""

import streamlit as st

# Color Palette - Navy Blue & White Professional Theme
COLORS = {
    "primary": "#1e3a5f",        # Navy Blue
    "primary_dark": "#0f2744",   # Dark Navy
    "primary_light": "#2c5282",  # Light Navy
    "secondary": "#3182ce",      # Accent Blue
    "white": "#ffffff",          # White
    "light_gray": "#f7fafc",     # Light Gray (backgrounds)
    "gray": "#718096",           # Medium Gray
    "dark_gray": "#2d3748",      # Dark Gray (text)
    "border": "#e2e8f0",         # Border Gray
    "success": "#38a169",        # Green
    "warning": "#d69e2e",        # Amber
    "danger": "#e53e3e",         # Red
}

def apply_custom_css():
    """Apply custom CSS styling for tab-based navigation."""

    st.markdown("""
    <style>
    /* ============================================
       GLOBAL STYLES
       ============================================ */

    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Root variables */
    :root {
        --navy: #1e3a5f;
        --navy-dark: #0f2744;
        --navy-light: #2c5282;
        --accent-blue: #3182ce;
        --white: #ffffff;
        --light-gray: #f7fafc;
        --gray: #718096;
        --dark-gray: #2d3748;
        --border: #e2e8f0;
        --success: #38a169;
        --warning: #d69e2e;
        --danger: #e53e3e;
    }

    /* Base styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f7fafc;
    }

    /* Hide the sidebar completely */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    section.main > div {
        max-width: 1400px;
        margin: 0 auto;
        padding: 1rem;
    }

    /* ============================================
       TAB STYLES
       ============================================ */

    /* Tab container */
    .stTabs {
        background: transparent;
    }

    /* Tab list container */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        gap: 0.25rem;
    }

    /* Individual tabs */
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        color: #4a5568;
        background: transparent;
        transition: all 0.2s ease;
    }

    /* Tab hover state */
    .stTabs [data-baseweb="tab"]:hover {
        background: #f7fafc;
        color: #1e3a5f;
    }

    /* Active tab */
    .stTabs [aria-selected="true"] {
        background: #1e3a5f !important;
        color: white !important;
    }

    /* Tab panel */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem;
    }

    /* ============================================
       BUTTON STYLES
       ============================================ */

    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
        border: none;
    }

    .stButton > button[kind="primary"] {
        background-color: #1e3a5f;
        color: white;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #0f2744;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.2);
    }

    .stButton > button[kind="secondary"] {
        background: white;
        color: #1e3a5f;
        border: 2px solid #1e3a5f;
    }

    .stButton > button[kind="secondary"]:hover {
        background: #1e3a5f;
        color: white;
    }

    /* ============================================
       FORM & INPUT STYLES
       ============================================ */

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        border-radius: 6px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 0.625rem 1rem !important;
        transition: border-color 0.2s ease;
        font-family: 'Inter', sans-serif;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #1e3a5f !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 95, 0.1) !important;
    }

    /* Labels */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stTextArea label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }

    /* ============================================
       DATAFRAME & TABLE STYLES
       ============================================ */

    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    [data-testid="stDataFrameContainer"] {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }

    /* ============================================
       EXPANDER STYLES
       ============================================ */

    .streamlit-expanderHeader {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-weight: 600;
        color: #1e3a5f;
        padding: 1rem !important;
    }

    .streamlit-expanderHeader:hover {
        background-color: #f7fafc;
    }

    .streamlit-expanderContent {
        border: 1px solid #e2e8f0;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem;
        background: white;
    }

    /* ============================================
       ALERT & MESSAGE STYLES
       ============================================ */

    .stAlert {
        border-radius: 8px;
        border: none;
        padding: 1rem;
    }

    /* Success alert */
    .stAlert[data-baseweb="notification"][kind="success"] {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
    }

    /* Info alert */
    .stAlert[data-baseweb="notification"][kind="info"] {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
    }

    /* Warning alert */
    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
    }

    /* Error alert */
    .stAlert[data-baseweb="notification"][kind="error"] {
        background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
        color: white;
    }

    /* ============================================
       METRIC STYLES
       ============================================ */

    [data-testid="stMetric"] {
        background: white;
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    [data-testid="stMetricLabel"] {
        color: #718096 !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em;
    }

    [data-testid="stMetricValue"] {
        color: #1e3a5f !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }

    /* ============================================
       RESPONSIVE ADJUSTMENTS
       ============================================ */

    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto;
            white-space: nowrap;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    </style>
    """, unsafe_allow_html=True)


def get_page_header_style():
    """Return the standard page header style."""
    return """
        background-color: #1e3a5f;
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    """


def get_card_style():
    """Return the standard card style."""
    return """
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    """


def get_stat_card_style(variant="primary"):
    """Return stat card style based on variant."""
    colors = {
        "primary": "#1e3a5f",
        "success": "#38a169",
        "warning": "#d69e2e",
        "danger": "#e53e3e",
        "info": "#3182ce",
    }
    bg_color = colors.get(variant, "#1e3a5f")
    return f"""
        background: linear-gradient(135deg, {bg_color} 0%, {bg_color}dd 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
        cursor: default;
    """