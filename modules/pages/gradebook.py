import streamlit as st
import pandas as pd
from io import BytesIO
from modules import database as db

def render():
    st.title("📊 Gradebook")

    # Get all classes
    classes = db.get_all_classes()
    if not classes:
        st.warning("No classes found. Please create a class first.")
        return

    class_options = {c['name']: c['id'] for c in classes}
    selected_class_name = st.selectbox(
        "Select Class",
        options=list(class_options.keys()),
        key="gradebook_class_select"
    )
    selected_class_id = class_options[selected_class_name]

    st.markdown("---")

    # Get students and assignments
    students = db.get_students_by_class(selected_class_id)
    assignments = db.get_assignments_by_class(selected_class_id)

    if not students:
        st.warning("No students in this class.")
        return

    if not assignments:
        st.warning("No assignments for this class.")
        return

    # Get grade scale
    grade_scale = db.get_grade_scale()

    # Build gradebook matrix
    gradebook_data = []

    for student in students:
        row = {"Student": student['name'], "student_id": student['id']}
        total_weighted = 0
        total_weight = 0

        for assignment in assignments:
            grade = db.get_grade(student['id'], assignment['id'])
            if grade and grade['points'] is not None:
                points = grade['points']
                percentage = (points / assignment['max_points']) * 100
                row[assignment['name']] = f"{points:.1f}"
                total_weighted += percentage * assignment['weight']
                total_weight += assignment['weight']
            else:
                row[assignment['name']] = "-"

        # Calculate weighted average
        if total_weight > 0:
            weighted_avg = total_weighted / total_weight
            row['Average'] = f"{weighted_avg:.1f}%"
            row['Letter'] = get_letter_grade(weighted_avg, grade_scale)
            row['_avg_value'] = weighted_avg  # For sorting
        else:
            row['Average'] = "-"
            row['Letter'] = "-"
            row['_avg_value'] = -1

        gradebook_data.append(row)

    df = pd.DataFrame(gradebook_data)

    # Configure columns
    column_config = {
        "student_id": None,
        "_avg_value": None,
        "Student": st.column_config.TextColumn("Student", width="large"),
        "Average": st.column_config.TextColumn("Average", width="small"),
        "Letter": st.column_config.TextColumn("Grade", width="small"),
    }

    for a in assignments:
        column_config[a['name']] = st.column_config.TextColumn(
            a['name'],
            help=f"Max: {a['max_points']} pts, Weight: {a['weight']}",
            width="small"
        )

    # Display gradebook
    st.subheader(f"Grades for {selected_class_name}")

    # Highlight missing assignments
    def highlight_missing(val):
        if val == "-":
            return "background-color: #ffcccc"
        return ""

    display_cols = ['Student'] + [a['name'] for a in assignments] + ['Average', 'Letter']
    display_df = df[display_cols]

    st.dataframe(
        display_df.style.applymap(highlight_missing),
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )

    # Class statistics
    st.markdown("---")
    st.subheader("📈 Class Statistics")

    valid_avgs = [row['_avg_value'] for row in gradebook_data if row['_avg_value'] >= 0]

    if valid_avgs:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Class Average", f"{sum(valid_avgs)/len(valid_avgs):.1f}%")
        with col2:
            st.metric("Highest", f"{max(valid_avgs):.1f}%")
        with col3:
            st.metric("Lowest", f"{min(valid_avgs):.1f}%")
        with col4:
            passing = sum(1 for avg in valid_avgs if avg >= 60)
            st.metric("Passing", f"{passing}/{len(valid_avgs)}")

        # Grade distribution
        st.subheader("Grade Distribution")
        grade_counts = {}
        for avg in valid_avgs:
            letter = get_letter_grade(avg, grade_scale)
            grade_counts[letter] = grade_counts.get(letter, 0) + 1

        dist_df = pd.DataFrame([
            {"Grade": grade, "Count": count}
            for grade, count in sorted(grade_counts.items())
        ])

        if not dist_df.empty:
            st.bar_chart(dist_df.set_index('Grade'))

    # Export section
    st.markdown("---")
    st.subheader("📥 Export")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Export to Excel", use_container_width=True):
            excel_buffer = export_to_excel(display_df, selected_class_name)
            st.download_button(
                label="Download Excel",
                data=excel_buffer,
                file_name=f"gradebook_{selected_class_name.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    with col2:
        if st.button("📄 Export to CSV", use_container_width=True):
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"gradebook_{selected_class_name.replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    with col3:
        if st.button("📋 Class Summary", use_container_width=True):
            summary = generate_class_summary(gradebook_data, assignments, grade_scale, selected_class_name)
            st.download_button(
                label="Download Summary",
                data=summary,
                file_name=f"summary_{selected_class_name.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )


def get_letter_grade(percentage, scale):
    """Convert percentage to letter grade based on scale."""
    if percentage >= scale.get('A', 90):
        return 'A'
    elif percentage >= scale.get('B', 80):
        return 'B'
    elif percentage >= scale.get('C', 70):
        return 'C'
    elif percentage >= scale.get('D', 60):
        return 'D'
    else:
        return 'F'


def export_to_excel(df, class_name):
    """Export gradebook to Excel."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=class_name[:31], index=False)
    buffer.seek(0)
    return buffer


def generate_class_summary(gradebook_data, assignments, grade_scale, class_name):
    """Generate a text summary of class grades."""
    valid_avgs = [row['_avg_value'] for row in gradebook_data if row['_avg_value'] >= 0]

    summary = f"""
CLASS SUMMARY REPORT
====================
Class: {class_name}
Total Students: {len(gradebook_data)}
Total Assignments: {len(assignments)}

GRADE STATISTICS
----------------
"""
    if valid_avgs:
        summary += f"""Class Average: {sum(valid_avgs)/len(valid_avgs):.1f}%
Highest Score: {max(valid_avgs):.1f}%
Lowest Score: {min(valid_avgs):.1f}%
Passing Rate: {sum(1 for avg in valid_avgs if avg >= 60)}/{len(valid_avgs)} ({100*sum(1 for avg in valid_avgs if avg >= 60)/len(valid_avgs):.0f}%)

GRADE DISTRIBUTION
------------------
"""
        grade_counts = {}
        for avg in valid_avgs:
            letter = get_letter_grade(avg, grade_scale)
            grade_counts[letter] = grade_counts.get(letter, 0) + 1

        for grade in ['A', 'B', 'C', 'D', 'F']:
            count = grade_counts.get(grade, 0)
            summary += f"{grade}: {count} students\n"

    summary += f"""
ASSIGNMENTS
-----------
"""
    for a in assignments:
        summary += f"- {a['name']}: {a['max_points']} pts (weight: {a['weight']})\n"

    summary += f"""
STUDENT GRADES
--------------
"""
    for row in sorted(gradebook_data, key=lambda x: x['Student']):
        summary += f"{row['Student']}: {row['Average']} ({row['Letter']})\n"

    return summary
