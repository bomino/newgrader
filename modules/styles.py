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

    # Add a floating menu button - only visible when sidebar is collapsed
    st.markdown("""
    <div id="floating-menu-btn" onclick="openSidebar()" style="
        position: fixed;
        left: 8px;
        top: 14px;
        width: 40px;
        height: 40px;
        background-color: #1e3a5f;
        border: 2px solid #3182ce;
        border-radius: 8px;
        cursor: pointer;
        z-index: 999999;
        display: none;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    ">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
    </div>

    <script>
    function openSidebar() {
        console.log('Opening sidebar...');

        // Method 1: Find and click the collapsed control button
        const collapsedControl = document.querySelector('[data-testid="collapsedControl"]');
        if (collapsedControl) {
            console.log('Found collapsedControl');
            const btn = collapsedControl.querySelector('button') || collapsedControl;
            btn.click();
            return;
        }

        // Method 2: Find button with specific test id
        const baseButton = document.querySelector('[data-testid="baseButton-header"]');
        if (baseButton) {
            console.log('Found baseButton-header');
            baseButton.click();
            return;
        }

        // Method 3: Find the expand icon button
        const allButtons = document.querySelectorAll('button');
        for (let btn of allButtons) {
            const svg = btn.querySelector('svg');
            const ariaLabel = btn.getAttribute('aria-label') || '';
            const title = btn.getAttribute('title') || '';

            if (ariaLabel.toLowerCase().includes('expand') ||
                title.toLowerCase().includes('expand') ||
                ariaLabel.toLowerCase().includes('open') ||
                title.toLowerCase().includes('open')) {
                console.log('Found expand button via aria-label/title');
                btn.click();
                return;
            }
        }

        // Method 4: Directly manipulate sidebar CSS
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const sidebarContent = document.querySelector('[data-testid="stSidebarContent"]');

        if (sidebar) {
            console.log('Forcing sidebar open via CSS');
            sidebar.style.width = '336px';
            sidebar.style.minWidth = '336px';
            sidebar.style.transform = 'none';
            sidebar.style.marginLeft = '0';
            sidebar.setAttribute('aria-expanded', 'true');

            // Also try to find parent container
            const sidebarNav = sidebar.closest('[data-testid="stSidebarNav"]') ||
                              sidebar.parentElement;
            if (sidebarNav) {
                sidebarNav.style.width = '336px';
                sidebarNav.style.transform = 'none';
            }
        }

        // Method 5: Trigger resize event (sometimes helps Streamlit recalculate)
        window.dispatchEvent(new Event('resize'));
    }

    // Check sidebar state and show/hide hamburger button
    function checkSidebarState() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const floatingBtn = document.getElementById('floating-menu-btn');

        if (!floatingBtn) return;

        if (sidebar) {
            const rect = sidebar.getBoundingClientRect();
            const isVisible = rect.width > 50 && rect.left >= -10;
            floatingBtn.style.display = isVisible ? 'none' : 'flex';
        } else {
            // No sidebar found, show the button
            floatingBtn.style.display = 'flex';
        }
    }

    // Check sidebar state periodically
    setInterval(checkSidebarState, 300);

    // Initial checks
    setTimeout(checkSidebarState, 500);
    setTimeout(checkSidebarState, 1000);
    setTimeout(checkSidebarState, 2000);
    </script>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* ============================================
       FLOATING MENU BUTTON
       ============================================ */

    #floating-menu-btn:hover {
        background-color: #3182ce !important;
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
    }

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

    /* Sidebar collapse/expand button - make it VERY visible */
    [data-testid="collapsedControl"] {
        background-color: #1e3a5f !important;
        border: 3px solid #3182ce !important;
        border-left: none !important;
        border-radius: 0 12px 12px 0 !important;
        width: 44px !important;
        height: 80px !important;
        left: 0 !important;
        top: 120px !important;
        position: fixed !important;
        z-index: 999999 !important;
        box-shadow: 4px 4px 16px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        animation: pulse-glow 2s ease-in-out infinite !important;
    }

    @keyframes pulse-glow {
        0%, 100% {
            box-shadow: 4px 4px 16px rgba(0, 0, 0, 0.4), 0 0 8px rgba(49, 130, 206, 0.5);
        }
        50% {
            box-shadow: 4px 4px 20px rgba(0, 0, 0, 0.5), 0 0 20px rgba(49, 130, 206, 0.8);
        }
    }

    [data-testid="collapsedControl"]:hover {
        background-color: #3182ce !important;
        border-color: #1e3a5f !important;
        width: 52px !important;
        box-shadow: 6px 6px 24px rgba(0, 0, 0, 0.5) !important;
        animation: none !important;
    }

    [data-testid="collapsedControl"] svg {
        color: white !important;
        stroke: white !important;
        fill: white !important;
        width: 28px !important;
        height: 28px !important;
    }

    /* Style the button inside collapsed control */
    [data-testid="collapsedControl"] button {
        background: transparent !important;
        border: none !important;
        width: 100% !important;
        height: 100% !important;
        cursor: pointer !important;
    }

    /* When sidebar is collapsed, ensure button is always visible */
    [data-testid="stSidebar"][aria-expanded="false"] ~ [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* Also target the sidebar header close button */
    [data-testid="stSidebar"] button[kind="headerNoPadding"],
    [data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-radius: 6px !important;
        width: 36px !important;
        height: 36px !important;
    }

    [data-testid="stSidebar"] button[kind="headerNoPadding"]:hover,
    [data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"]:hover {
        background-color: rgba(255, 255, 255, 0.3) !important;
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
