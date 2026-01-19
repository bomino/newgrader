import streamlit as st
import pandas as pd
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
        <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700;">Grade Entry</h1>
        <p style="margin: 0.25rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">Enter and manage student grades</p>
    </div>
    """, unsafe_allow_html=True)

    classes = db.get_all_classes()

    if not classes:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 4rem 2rem;
            background: white;
            border-radius: 8px;
            border: 2px dashed #e2e8f0;
        ">
            <h3 style="color: #1e3a5f; margin-bottom: 0.5rem;">No Classes Found</h3>
            <p style="color: #718096;">Create a class first to enter grades.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Selectors
    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 0.95rem;">Select Class & Assignment</h4>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        class_options = {c['name']: c['id'] for c in classes}
        selected_class_name = st.selectbox(
            "Select Class",
            options=list(class_options.keys()),
            key="grade_entry_class_select"
        )
        selected_class_id = class_options[selected_class_name]

    assignments = db.get_assignments_by_class(selected_class_id)

    if not assignments:
        st.warning(f"No assignments found for {selected_class_name}. Create an assignment first.")
        return

    with col2:
        assignment_options = {f"{a['name']} ({a['max_points']} pts)": a['id'] for a in assignments}
        selected_assignment_key = st.selectbox(
            "Select Assignment",
            options=list(assignment_options.keys()),
            key="grade_entry_assignment_select"
        )
        selected_assignment_id = assignment_options[selected_assignment_key]
        selected_assignment = db.get_assignment_by_id(selected_assignment_id)

    students = db.get_students_by_class(selected_class_id)

    if not students:
        st.warning(f"No students in {selected_class_name}. Add students first.")
        return

    # Assignment info
    st.markdown(f"""
    <div style="
        background: #f7fafc;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    ">
        <h3 style="margin: 0 0 0.25rem 0; color: #1e3a5f; font-size: 1rem;">{selected_assignment['name']}</h3>
        <div style="color: #718096; font-size: 0.9rem;">
            Max Points: <strong>{selected_assignment['max_points']}</strong> | Weight: <strong>{selected_assignment['weight']}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Get existing grades
    existing_grades = {g['student_id']: g for g in db.get_grades_by_assignment(selected_assignment_id)}

    # Create form data
    grade_data = []
    for student in students:
        existing = existing_grades.get(student['id'], {})
        grade_data.append({
            "student_id": student['id'],
            "Student Name": student['name'],
            "Points": existing.get('points', None),
            "Comments": existing.get('comments', "") or ""
        })

    df = pd.DataFrame(grade_data)

    st.markdown("""
    <div style="
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e2e8f0;
        border-bottom: none;
    ">
        <h4 style="margin: 0; color: #1e3a5f; font-size: 1rem;">Enter Grades</h4>
    </div>
    """, unsafe_allow_html=True)

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        disabled=["student_id", "Student Name"],
        column_config={
            "student_id": None,
            "Student Name": st.column_config.TextColumn("Student Name", width="large"),
            "Points": st.column_config.NumberColumn(
                "Points",
                min_value=0.0,
                max_value=float(selected_assignment['max_points']),
                step=0.5,
                width="medium"
            ),
            "Comments": st.column_config.TextColumn("Comments", width="large")
        },
        key="grade_editor"
    )

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Save All Grades", type="primary", use_container_width=True):
            grades_to_save = []
            for idx, row in edited_df.iterrows():
                if row['Points'] is not None:
                    grades_to_save.append({
                        'student_id': row['student_id'],
                        'assignment_id': selected_assignment_id,
                        'points': row['Points'],
                        'comments': row['Comments'] if row['Comments'] else None
                    })

            if grades_to_save:
                db.bulk_set_grades(grades_to_save)
                st.success(f"Saved {len(grades_to_save)} grades!")
                st.rerun()
            else:
                st.warning("No grades to save.")

    with col2:
        if st.button("Reset", use_container_width=True):
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick stats
    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    ">
        <h3 style="margin: 0 0 1rem 0; color: #1e3a5f; font-size: 1rem;">Quick Stats</h3>
    </div>
    """, unsafe_allow_html=True)

    graded_count = len([g for g in existing_grades.values() if g.get('points') is not None])
    total_students = len(students)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="
            background: #1e3a5f;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 1.5rem; font-weight: 700;">{graded_count}/{total_students}</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Graded</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if graded_count > 0:
            avg_score = sum(g['points'] for g in existing_grades.values() if g.get('points') is not None) / graded_count
            avg_display = f"{avg_score:.1f}"
        else:
            avg_display = "-"

        st.markdown(f"""
        <div style="
            background: #38a169;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 1.5rem; font-weight: 700;">{avg_display}</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Average</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if graded_count > 0:
            max_score = max(g['points'] for g in existing_grades.values() if g.get('points') is not None)
            high_display = f"{max_score:.1f}"
        else:
            high_display = "-"

        st.markdown(f"""
        <div style="
            background: #3182ce;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 1.5rem; font-weight: 700;">{high_display}</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Highest</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        if graded_count > 0:
            min_score = min(g['points'] for g in existing_grades.values() if g.get('points') is not None)
            low_display = f"{min_score:.1f}"
        else:
            low_display = "-"

        st.markdown(f"""
        <div style="
            background: #e53e3e;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 1.5rem; font-weight: 700;">{low_display}</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Lowest</div>
        </div>
        """, unsafe_allow_html=True)
