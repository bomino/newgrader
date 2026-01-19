import streamlit as st
from modules import database as db

def render():
    st.title("⚙️ Settings")

    # Grade Scale Configuration
    st.subheader("📊 Grade Scale")
    st.caption("Configure the percentage thresholds for letter grades.")

    current_scale = db.get_grade_scale()

    with st.form("grade_scale_form"):
        col1, col2 = st.columns(2)

        with col1:
            a_threshold = st.number_input(
                "A minimum %",
                min_value=0,
                max_value=100,
                value=current_scale.get('A', 90),
                step=1,
                help="Scores at or above this percentage receive an A"
            )
            b_threshold = st.number_input(
                "B minimum %",
                min_value=0,
                max_value=100,
                value=current_scale.get('B', 80),
                step=1,
                help="Scores at or above this percentage receive a B"
            )
            c_threshold = st.number_input(
                "C minimum %",
                min_value=0,
                max_value=100,
                value=current_scale.get('C', 70),
                step=1,
                help="Scores at or above this percentage receive a C"
            )

        with col2:
            d_threshold = st.number_input(
                "D minimum %",
                min_value=0,
                max_value=100,
                value=current_scale.get('D', 60),
                step=1,
                help="Scores at or above this percentage receive a D"
            )
            st.info("Scores below D threshold receive an F")

        # Validation
        submitted = st.form_submit_button("💾 Save Grade Scale", use_container_width=True)

        if submitted:
            # Validate thresholds are in descending order
            if a_threshold > b_threshold > c_threshold > d_threshold:
                new_scale = {
                    'A': a_threshold,
                    'B': b_threshold,
                    'C': c_threshold,
                    'D': d_threshold,
                    'F': 0
                }
                db.set_grade_scale(new_scale)
                st.success("Grade scale saved!")
            else:
                st.error("Thresholds must be in descending order: A > B > C > D")

    # Preview grade scale
    st.markdown("---")
    st.subheader("Current Grade Scale Preview")

    scale = db.get_grade_scale()
    preview_data = [
        f"**A**: {scale.get('A', 90)}% - 100%",
        f"**B**: {scale.get('B', 80)}% - {scale.get('A', 90) - 1}%",
        f"**C**: {scale.get('C', 70)}% - {scale.get('B', 80) - 1}%",
        f"**D**: {scale.get('D', 60)}% - {scale.get('C', 70) - 1}%",
        f"**F**: 0% - {scale.get('D', 60) - 1}%"
    ]

    for item in preview_data:
        st.write(item)

    # Database info
    st.markdown("---")
    st.subheader("📁 Database Information")

    counts = db.get_total_counts()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Classes", counts.get("classes", 0))
    with col2:
        st.metric("Students", counts.get("students", 0))
    with col3:
        st.metric("Assignments", counts.get("assignments", 0))

    st.caption(f"Database location: data/grader.db")

    # Reset section
    st.markdown("---")
    st.subheader("🔄 Reset Options")

    st.warning("These actions cannot be undone!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reset Grade Scale to Default", use_container_width=True):
            default_scale = {"A": 90, "B": 80, "C": 70, "D": 60, "F": 0}
            db.set_grade_scale(default_scale)
            st.success("Grade scale reset to default!")
            st.rerun()

    # About section
    st.markdown("---")
    st.subheader("ℹ️ About NewGrader")

    st.markdown("""
    **NewGrader** is a teacher grading application that helps you:

    - Manage classes and students
    - Create and track assignments
    - Enter grades manually or use auto-grading
    - View comprehensive gradebook with statistics
    - Export reports to Excel/CSV

    Built with Streamlit and SQLite.
    """)
