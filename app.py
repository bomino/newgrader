import streamlit as st
from modules import database as db
from modules import styles
from modules.pages import classes, students, assignments, grade_entry, auto_grade, gradebook, settings

# Page configuration
st.set_page_config(
    page_title="NewGrader",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
styles.apply_custom_css()

# Navigation
PAGES = {
    "Home": "home",
    "Classes": "classes",
    "Students": "students",
    "Assignments": "assignments",
    "Grade Entry": "grade_entry",
    "Auto-Grade": "auto_grade",
    "Gradebook": "gradebook",
    "Settings": "settings",
}

def render_home():
    """Render the home dashboard."""

    # Hero Header
    st.markdown("""
    <div style="
        background-color: #1e3a5f;
        color: white;
        padding: 2.5rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    ">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 700;">NewGrader</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Professional Grading System for Educators</p>
    </div>
    """, unsafe_allow_html=True)

    # Statistics Cards
    counts = db.get_total_counts()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="
            background-color: #1e3a5f;
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 2rem; font-weight: 700;">{counts.get('classes', 0)}</div>
            <div style="font-size: 0.875rem; opacity: 0.9;">Classes</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background-color: #3182ce;
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 2rem; font-weight: 700;">{counts.get('students', 0)}</div>
            <div style="font-size: 0.875rem; opacity: 0.9;">Students</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background-color: #2c5282;
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 2rem; font-weight: 700;">{counts.get('assignments', 0)}</div>
            <div style="font-size: 0.875rem; opacity: 0.9;">Assignments</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        total_possible = counts.get('students', 0) * counts.get('assignments', 0)
        st.markdown(f"""
        <div style="
            background-color: #0f2744;
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 2rem; font-weight: 700;">{total_possible}</div>
            <div style="font-size: 0.875rem; opacity: 0.9;">Total Grades</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Actions and Features
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            height: 100%;
        ">
            <h3 style="margin: 0 0 1rem 0; color: #1e3a5f; font-size: 1.1rem;">
                Quick Start Guide
            </h3>
            <div style="color: #2d3748; line-height: 2;">
                <div><strong>1.</strong> Create a class in <strong>Classes</strong></div>
                <div><strong>2.</strong> Add students to your class</div>
                <div><strong>3.</strong> Create assignments with weights</div>
                <div><strong>4.</strong> Enter grades or use auto-grading</div>
                <div><strong>5.</strong> View gradebook & export reports</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            height: 100%;
        ">
            <h3 style="margin: 0 0 1rem 0; color: #1e3a5f; font-size: 1.1rem;">
                Features
            </h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; color: #2d3748;">
                <div>Class Management</div>
                <div>Student Roster</div>
                <div>Assignments</div>
                <div>Grade Entry</div>
                <div>Auto-Grading</div>
                <div>Gradebook</div>
                <div>CSV Import</div>
                <div>Excel Export</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent Activity Section (if data exists)
    if counts.get('classes', 0) > 0:
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        ">
            <h3 style="margin: 0 0 1rem 0; color: #1e3a5f; font-size: 1.1rem;">
                Your Classes
            </h3>
        </div>
        """, unsafe_allow_html=True)

        classes_list = db.get_all_classes()
        cols = st.columns(min(len(classes_list), 4))

        for i, cls in enumerate(classes_list[:4]):
            student_count = db.get_student_count_by_class(cls['id'])
            assignments_count = len(db.get_assignments_by_class(cls['id']))

            with cols[i % 4]:
                st.markdown(f"""
                <div style="
                    background: #f7fafc;
                    padding: 1rem;
                    border-radius: 8px;
                    border: 1px solid #e2e8f0;
                    margin-top: -0.5rem;
                ">
                    <h4 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">{cls['name']}</h4>
                    <div style="font-size: 0.85rem; color: #718096;">
                        {student_count} students | {assignments_count} assignments
                    </div>
                </div>
                """, unsafe_allow_html=True)


def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0;">
            <div style="font-size: 1.5rem; font-weight: 700; color: white; margin-bottom: 0.25rem;">
                NewGrader
            </div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">Professional Grading System</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        selection = st.radio(
            "Navigation",
            list(PAGES.keys()),
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Sidebar stats
        counts = db.get_total_counts()
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.1);
            padding: 1rem;
            border-radius: 6px;
            margin-top: 1rem;
        ">
            <div style="color: rgba(255,255,255,0.7); font-size: 0.75rem; margin-bottom: 0.5rem; text-transform: uppercase;">Quick Stats</div>
            <div style="color: white; font-size: 0.9rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span>Classes</span><span style="font-weight: 600;">{counts.get('classes', 0)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span>Students</span><span style="font-weight: 600;">{counts.get('students', 0)}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Assignments</span><span style="font-weight: 600;">{counts.get('assignments', 0)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Main content routing
    if selection == "Home":
        render_home()
    elif selection == "Classes":
        classes.render()
    elif selection == "Students":
        students.render()
    elif selection == "Assignments":
        assignments.render()
    elif selection == "Grade Entry":
        grade_entry.render()
    elif selection == "Auto-Grade":
        auto_grade.render()
    elif selection == "Gradebook":
        gradebook.render()
    elif selection == "Settings":
        settings.render()


if __name__ == "__main__":
    main()
