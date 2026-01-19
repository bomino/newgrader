import streamlit as st
import pandas as pd
from modules import database as db

def render():
    st.title("✏️ Grade Entry")

    # Get all classes
    classes = db.get_all_classes()

    if not classes:
        st.warning("No classes found. Please create a class first.")
        return

    # Class selector
    class_options = {c['name']: c['id'] for c in classes}
    selected_class_name = st.selectbox(
        "Select Class",
        options=list(class_options.keys()),
        key="grade_entry_class_select"
    )
    selected_class_id = class_options[selected_class_name]

    # Get assignments for selected class
    assignments = db.get_assignments_by_class(selected_class_id)

    if not assignments:
        st.warning(f"No assignments found for {selected_class_name}. Please create an assignment first.")
        return

    # Assignment selector
    assignment_options = {f"{a['name']} ({a['max_points']} pts)": a['id'] for a in assignments}
    selected_assignment_key = st.selectbox(
        "Select Assignment",
        options=list(assignment_options.keys()),
        key="grade_entry_assignment_select"
    )
    selected_assignment_id = assignment_options[selected_assignment_key]
    selected_assignment = db.get_assignment_by_id(selected_assignment_id)

    st.markdown("---")

    # Get students in class
    students = db.get_students_by_class(selected_class_id)

    if not students:
        st.warning(f"No students in {selected_class_name}. Please add students first.")
        return

    st.subheader(f"Enter Grades for: {selected_assignment['name']}")
    st.caption(f"Max Points: {selected_assignment['max_points']}")

    # Build grade entry form
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

    # Use data editor for grade entry
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        disabled=["student_id", "Student Name"],
        column_config={
            "student_id": None,  # Hide this column
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

    # Save button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("💾 Save All Grades", type="primary", use_container_width=True):
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
                st.warning("No grades to save. Please enter at least one grade.")

    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()

    # Quick stats
    st.markdown("---")
    st.subheader("📊 Quick Stats")

    graded_count = len([g for g in existing_grades.values() if g.get('points') is not None])
    total_students = len(students)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Graded", f"{graded_count}/{total_students}")
    with col2:
        if graded_count > 0:
            avg_score = sum(g['points'] for g in existing_grades.values() if g.get('points') is not None) / graded_count
            avg_percent = (avg_score / selected_assignment['max_points']) * 100
            st.metric("Average", f"{avg_score:.1f} ({avg_percent:.0f}%)")
        else:
            st.metric("Average", "-")
    with col3:
        if graded_count > 0:
            max_score = max(g['points'] for g in existing_grades.values() if g.get('points') is not None)
            st.metric("Highest", f"{max_score:.1f}")
        else:
            st.metric("Highest", "-")
    with col4:
        if graded_count > 0:
            min_score = min(g['points'] for g in existing_grades.values() if g.get('points') is not None)
            st.metric("Lowest", f"{min_score:.1f}")
        else:
            st.metric("Lowest", "-")
