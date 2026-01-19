import streamlit as st

st.set_page_config(
    page_title="NewGrader",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def main():
    st.sidebar.title("📚 NewGrader")
    st.sidebar.markdown("---")

    selection = st.sidebar.radio("Navigation", list(PAGES.keys()))

    st.sidebar.markdown("---")
    st.sidebar.caption("Teacher Grading Application")

    # Main content area
    if selection == "Home":
        st.title("Welcome to NewGrader")
        st.markdown("""
        ### Your Personal Grading Assistant

        **Features:**
        - 📋 **Classes** - Manage your classes
        - 👥 **Students** - Add and organize students
        - 📝 **Assignments** - Create and track assignments
        - ✏️ **Grade Entry** - Enter grades manually
        - 🤖 **Auto-Grade** - Grade using answer keys
        - 📊 **Gradebook** - View all grades and calculations
        - ⚙️ **Settings** - Configure grade scales

        ---
        *Select a page from the sidebar to get started.*
        """)

        # Quick stats placeholder
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Classes", "0")
        with col2:
            st.metric("Students", "0")
        with col3:
            st.metric("Assignments", "0")
    else:
        st.title(selection)
        st.info(f"The {selection} page will be implemented soon.")

if __name__ == "__main__":
    main()
