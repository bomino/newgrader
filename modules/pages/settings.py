import streamlit as st
from modules import database as db

def render():
    # Page header
    st.markdown("""
    <div style="
        background-color: #1e3a5f;
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    ">
        <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700; color: white;">Settings</h1>
        <p style="margin: 0.25rem 0 0 0; opacity: 0.9; font-size: 0.95rem; color: white;">Configure your grading preferences</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Grade Scale Configuration
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-bottom: 1.5rem;
        ">
            <h3 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">Grade Scale Configuration</h3>
            <p style="color: #718096; font-size: 0.85rem; margin: 0;">
                Set the percentage thresholds for each letter grade.
            </p>
        </div>
        """, unsafe_allow_html=True)

        current_scale = db.get_grade_scale()

        with st.form("grade_scale_form"):
            col_a, col_b, col_c, col_d = st.columns(4)

            with col_a:
                st.markdown("""
                <div style="
                    background: #38a169;
                    color: white;
                    padding: 0.5rem;
                    border-radius: 6px;
                    text-align: center;
                    font-weight: 700;
                    margin-bottom: 0.5rem;
                    color: white;
                ">A</div>
                """, unsafe_allow_html=True)
                a_threshold = st.number_input(
                    "A min %",
                    min_value=0,
                    max_value=100,
                    value=current_scale.get('A', 90),
                    step=1,
                    label_visibility="collapsed"
                )

            with col_b:
                st.markdown("""
                <div style="
                    background: #3182ce;
                    color: white;
                    padding: 0.5rem;
                    border-radius: 6px;
                    text-align: center;
                    font-weight: 700;
                    margin-bottom: 0.5rem;
                    color: white;
                ">B</div>
                """, unsafe_allow_html=True)
                b_threshold = st.number_input(
                    "B min %",
                    min_value=0,
                    max_value=100,
                    value=current_scale.get('B', 80),
                    step=1,
                    label_visibility="collapsed"
                )

            with col_c:
                st.markdown("""
                <div style="
                    background: #d69e2e;
                    color: white;
                    padding: 0.5rem;
                    border-radius: 6px;
                    text-align: center;
                    font-weight: 700;
                    margin-bottom: 0.5rem;
                    color: white;
                ">C</div>
                """, unsafe_allow_html=True)
                c_threshold = st.number_input(
                    "C min %",
                    min_value=0,
                    max_value=100,
                    value=current_scale.get('C', 70),
                    step=1,
                    label_visibility="collapsed"
                )

            with col_d:
                st.markdown("""
                <div style="
                    background: #dd6b20;
                    color: white;
                    padding: 0.5rem;
                    border-radius: 6px;
                    text-align: center;
                    font-weight: 700;
                    margin-bottom: 0.5rem;
                    color: white;
                ">D</div>
                """, unsafe_allow_html=True)
                d_threshold = st.number_input(
                    "D min %",
                    min_value=0,
                    max_value=100,
                    value=current_scale.get('D', 60),
                    step=1,
                    label_visibility="collapsed"
                )

            st.caption("Scores below D threshold receive an F")

            submitted = st.form_submit_button("Save Grade Scale", use_container_width=True, type="primary")

            if submitted:
                if a_threshold > b_threshold > c_threshold > d_threshold:
                    new_scale = {
                        'A': a_threshold,
                        'B': b_threshold,
                        'C': c_threshold,
                        'D': d_threshold,
                        'F': 0
                    }
                    db.set_grade_scale(new_scale)
                    st.success("Grade scale saved successfully!")
                else:
                    st.error("Thresholds must be in descending order: A > B > C > D")

    with col2:
        # Grade scale preview
        scale = db.get_grade_scale()

        st.markdown("""
        <div style="
            background: #f7fafc;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        ">
            <h4 style="margin: 0 0 1rem 0; color: #1e3a5f; font-size: 1rem;">Current Scale</h4>
        </div>
        """, unsafe_allow_html=True)

        grades_info = [
            ("A", scale.get('A', 90), 100, "#38a169"),
            ("B", scale.get('B', 80), scale.get('A', 90) - 1, "#3182ce"),
            ("C", scale.get('C', 70), scale.get('B', 80) - 1, "#d69e2e"),
            ("D", scale.get('D', 60), scale.get('C', 70) - 1, "#dd6b20"),
            ("F", 0, scale.get('D', 60) - 1, "#e53e3e"),
        ]

        for grade, min_val, max_val, color in grades_info:
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.5rem 0;
                border-bottom: 1px solid #e2e8f0;
            ">
                <span style="
                    background: {color};
                    color: white;
                    width: 32px;
                    height: 32px;
                    border-radius: 6px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 700;
                ">{grade}</span>
                <span style="color: #2d3748;">{min_val}% - {max_val}%</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Database info section
    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    ">
        <h3 style="margin: 0 0 1rem 0; color: #1e3a5f; font-size: 1rem;">Database Information</h3>
    </div>
    """, unsafe_allow_html=True)

    counts = db.get_total_counts()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="
            background: #1e3a5f;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 2rem; font-weight: 700; color: white;">{counts.get('classes', 0)}</div>
            <div style="font-size: 0.85rem; opacity: 0.9; color: white;">Classes</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background: #3182ce;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 2rem; font-weight: 700; color: white;">{counts.get('students', 0)}</div>
            <div style="font-size: 0.85rem; opacity: 0.9; color: white;">Students</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background: #2c5282;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 2rem; font-weight: 700; color: white;">{counts.get('assignments', 0)}</div>
            <div style="font-size: 0.85rem; opacity: 0.9; color: white;">Assignments</div>
        </div>
        """, unsafe_allow_html=True)

    st.caption("Database location: `data/grader.db`")

    st.markdown("<br>", unsafe_allow_html=True)

    # Reset section
    st.markdown("""
    <div style="
        background: #fff5f5;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #fed7d7;
    ">
        <h3 style="margin: 0 0 0.5rem 0; color: #c53030; font-size: 1rem;">Reset Options</h3>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Reset Grade Scale to Default", use_container_width=False):
        default_scale = {"A": 90, "B": 80, "C": 70, "D": 60, "F": 0}
        db.set_grade_scale(default_scale)
        st.success("Grade scale reset to default values!")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # About section
    st.markdown("""
    <div style="
        background-color: #1e3a5f;
        color: white;
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
    ">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.25rem; color: white;">Grader</h3>
        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem; color: white;">Professional Grading Application</p>
        <p style="margin: 1rem 0 0 0; font-size: 0.8rem; opacity: 0.7; color: white;">Built with Streamlit & SQLite</p>
    </div>
    """, unsafe_allow_html=True)
