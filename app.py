"""
Grader - Professional Grading System
Main application with tab-based navigation
"""

import streamlit as st
from modules import database as db
from modules import styles_tabbed as styles
from modules.pages import (
    classes, students, assignments,
    grade_entry, auto_grade, gradebook, settings, help_guide
)

# Page configuration
st.set_page_config(
    page_title="Grader - Professional Grading System",
    page_icon="📚",
    layout="wide"
)

# Initialize database
db.init_db()

# Apply custom CSS (without sidebar)
styles.apply_custom_css()

# Main header
st.markdown("""
<div style="
    background-color: #1e3a5f;
    color: white;
    padding: 1.5rem;
    margin: -1rem -1rem 2rem -1rem;
    text-align: center;
">
    <h1 style="margin: 0; font-size: 2.5rem; color: white;">📚 Grader</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; color: white;">Professional Grading System for Educators</p>
</div>
""", unsafe_allow_html=True)

# Tab-based navigation
tabs = st.tabs([
    "🏠 Home",
    "🎓 Classes",
    "👥 Students",
    "📝 Assignments",
    "✏️ Grade Entry",
    "🤖 Auto-Grade",
    "📊 Gradebook",
    "⚙️ Settings",
    "❓ Help"
])

# Home tab
with tabs[0]:
    st.markdown("""
    <div style="
        background-color: #f7fafc;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    ">
        <h2 style="color: #1e3a5f; margin-bottom: 1rem;">Welcome to Grader</h2>
        <p style="color: #4a5568; font-size: 1.1rem;">
            Streamline your grading process with our professional grading system.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)

    counts = db.get_total_counts()
    total_classes = counts.get("classes", 0)
    total_students = counts.get("students", 0)
    total_assignments = counts.get("assignments", 0)

    # Get total grades count separately
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM grades WHERE points IS NOT NULL")
        total_grades = cursor.fetchone()[0]

    with col1:
        st.markdown(f"""
        <div style="{styles.get_stat_card_style('primary')}">
            <h2 style="margin: 0; font-size: 2.5rem; color: white;">{total_classes}</h2>
            <p style="margin: 0.5rem 0 0 0; color: white;">Classes</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="{styles.get_stat_card_style('info')}">
            <h2 style="margin: 0; font-size: 2.5rem; color: white;">{total_students}</h2>
            <p style="margin: 0.5rem 0 0 0; color: white;">Students</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="{styles.get_stat_card_style('warning')}">
            <h2 style="margin: 0; font-size: 2.5rem; color: white;">{total_assignments}</h2>
            <p style="margin: 0.5rem 0 0 0; color: white;">Assignments</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="{styles.get_stat_card_style('success')}">
            <h2 style="margin: 0; font-size: 2.5rem; color: white;">{total_grades}</h2>
            <p style="margin: 0.5rem 0 0 0; color: white;">Total Grades</p>
        </div>
        """, unsafe_allow_html=True)

    # Quick Start Guide
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🚀 Quick Start Guide")
        st.markdown("""
        1. **Create a class** in the Classes tab
        2. **Add students** to your class in the Students tab
        3. **Create assignments** with weights in the Assignments tab
        4. **Enter grades** or use auto-grading
        5. **View gradebook** & export reports
        """)

    with col2:
        st.markdown("### ✨ Features")
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.markdown("""
            - Class Management
            - Assignments
            - Auto-Grading
            """)
        with col2_2:
            st.markdown("""
            - Student Roster
            - Grade Entry
            - Gradebook & Excel Export
            """)

    # Your Classes section
    st.markdown("---")
    st.markdown("### 📚 Your Classes")

    classes_list = db.get_all_classes()
    if classes_list:
        for class_item in classes_list:
            with st.container():
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 1rem;
                    border-radius: 8px;
                    border-left: 4px solid #1e3a5f;
                    margin-bottom: 0.5rem;
                ">
                    <h4 style="margin: 0; color: #1e3a5f;">{class_item['name']}</h4>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No classes yet. Go to the Classes tab to create your first class!")

# Classes tab
with tabs[1]:
    classes.render()

# Students tab
with tabs[2]:
    students.render()

# Assignments tab
with tabs[3]:
    assignments.render()

# Grade Entry tab
with tabs[4]:
    grade_entry.render()

# Auto-Grade tab
with tabs[5]:
    auto_grade.render()

# Gradebook tab
with tabs[6]:
    gradebook.render()

# Settings tab
with tabs[7]:
    settings.render()

# Help tab
with tabs[8]:
    help_guide.render()

# Footer
st.markdown("---")
st.markdown("""
<div style="
    background-color: #1e3a5f;
    color: white;
    padding: 2rem;
    margin: 2rem -1rem -1rem -1rem;
    text-align: center;
">
    <p style="margin: 0; opacity: 0.9; color: white;">
        © 2024 Grader • Professional Grading System • Built for Educators
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; opacity: 0.7; color: white;">
        Version 1.0 • All data stored locally
    </p>
</div>
""", unsafe_allow_html=True)