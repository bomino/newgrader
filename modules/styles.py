"""
NewGrader Custom Styling Module
Professional UI styling with Navy Blue & White theme
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
    """Apply custom CSS styling to the entire app."""
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

    /* ============================================
       SIDEBAR STYLES
       ============================================ */

    [data-testid="stSidebar"] {
        background-color: #1e3a5f;
    }

    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown span,
    [data-testid="stSidebar"] .stMarkdown div {
        color: white !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: all 0.2s ease;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] .stRadio label span {
        color: white !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h4 {
        color: white !important;
        font-weight: 700 !important;
    }

    /* Make all text elements in sidebar white */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    /* Sidebar collapse/expand button - make it very visible */
    [data-testid="collapsedControl"] {
        background-color: #1e3a5f !important;
        border: 2px solid #1e3a5f !important;
        border-radius: 0 8px 8px 0 !important;
        width: 32px !important;
        height: 48px !important;
        left: 0 !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="collapsedControl"]:hover {
        background-color: #2c5282 !important;
        border-color: #2c5282 !important;
        box-shadow: 3px 3px 12px rgba(0, 0, 0, 0.3) !important;
    }

    [data-testid="collapsedControl"] svg {
        color: white !important;
        stroke: white !important;
        width: 20px !important;
        height: 20px !important;
    }

    /* When sidebar is collapsed, make the button stand out more */
    [data-testid="stSidebar"][aria-expanded="false"] + [data-testid="collapsedControl"],
    button[kind="headerNoPadding"] {
        background-color: #1e3a5f !important;
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
    .stSelectbox > div > div > div {
        border-radius: 6px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 0.625rem 1rem !important;
        transition: border-color 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #1e3a5f !important;
        box-shadow: 0 0 0 2px rgba(30, 58, 95, 0.1) !important;
    }

    /* ============================================
       DATAFRAME & TABLE STYLES
       ============================================ */

    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    [data-testid="stDataFrameContainer"] {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }

    /* ============================================
       EXPANDER STYLES
       ============================================ */

    .streamlit-expanderHeader {
        background-color: #f7fafc;
        border-radius: 6px;
        font-weight: 600;
        color: #1e3a5f;
    }

    .streamlit-expanderContent {
        border: 1px solid #e2e8f0;
        border-top: none;
        border-radius: 0 0 6px 6px;
        padding: 1rem;
    }

    /* ============================================
       TAB STYLES
       ============================================ */

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f7fafc;
        padding: 4px;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        color: #1e3a5f;
    }

    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #1e3a5f !important;
        border-bottom: 2px solid #1e3a5f;
    }

    /* ============================================
       ALERT & MESSAGE STYLES
       ============================================ */

    .stAlert {
        border-radius: 6px;
        border: none;
    }

    /* ============================================
       METRIC STYLES
       ============================================ */

    [data-testid="stMetric"] {
        background: white;
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }

    [data-testid="stMetricLabel"] {
        color: #718096 !important;
        font-weight: 500 !important;
    }

    [data-testid="stMetricValue"] {
        color: #1e3a5f !important;
        font-weight: 700 !important;
    }

    /* ============================================
       RESPONSIVE ADJUSTMENTS
       ============================================ */

    @media (max-width: 768px) {
        .page-header {
            padding: 1.5rem;
        }

        .page-header h1 {
            font-size: 1.5rem;
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
        background-color: {bg_color};
        color: white;
        padding: 1.25rem;
        border-radius: 8px;
        text-align: center;
    """
