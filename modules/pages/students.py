import streamlit as st
import pandas as pd
from modules import database as db

def render():
    st.title("👥 Student Roster")

    # Get all classes
    classes = db.get_all_classes()

    if not classes:
        st.warning("No classes found. Please create a class first.")
        if st.button("Go to Classes"):
            st.session_state['nav_to'] = 'Classes'
            st.rerun()
        return

    # Class selector
    class_options = {c['name']: c['id'] for c in classes}
    selected_class_name = st.selectbox(
        "Select Class",
        options=list(class_options.keys()),
        key="student_class_select"
    )
    selected_class_id = class_options[selected_class_name]

    st.markdown("---")

    # Two columns: Add student form and bulk import
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("➕ Add Student")
        with st.form("add_student_form", clear_on_submit=True):
            student_name = st.text_input("Student Name", placeholder="e.g., John Smith")
            student_email = st.text_input("Email (optional)", placeholder="e.g., john@school.edu")
            submitted = st.form_submit_button("Add Student", use_container_width=True)

            if submitted:
                if student_name.strip():
                    db.add_student(
                        name=student_name.strip(),
                        class_id=selected_class_id,
                        email=student_email.strip() if student_email else None
                    )
                    st.success(f"Student '{student_name}' added!")
                    st.rerun()
                else:
                    st.warning("Please enter a student name.")

    with col2:
        st.subheader("📁 Bulk Import")
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="CSV should have columns: name (required), email (optional)"
        )

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.write(f"Preview ({len(df)} students):")
                st.dataframe(df.head(5), use_container_width=True, hide_index=True)

                if st.button("Import All Students", use_container_width=True):
                    students = df.to_dict('records')
                    added = db.bulk_add_students(students, selected_class_id)
                    st.success(f"Imported {added} students!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

    st.markdown("---")

    # Display students in selected class
    students = db.get_students_by_class(selected_class_id)

    if students:
        st.subheader(f"Students in {selected_class_name} ({len(students)})")

        # Create dataframe for display
        df = pd.DataFrame(students)
        df = df[['id', 'name', 'email', 'created_at']]
        df.columns = ['ID', 'Name', 'Email', 'Added']
        df['Added'] = df['Added'].apply(lambda x: x[:10] if x else 'N/A')
        df['Email'] = df['Email'].fillna('-')

        # Editable dataframe
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            disabled=['ID', 'Added'],
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Name": st.column_config.TextColumn("Name", width="large"),
                "Email": st.column_config.TextColumn("Email", width="medium"),
                "Added": st.column_config.TextColumn("Added", width="small")
            },
            key="student_editor"
        )

        # Save changes button
        if st.button("💾 Save Changes", use_container_width=True):
            # Update modified students
            for idx, row in edited_df.iterrows():
                original = df.iloc[idx]
                if row['Name'] != original['Name'] or row['Email'] != original['Email']:
                    email = row['Email'] if row['Email'] != '-' else None
                    db.update_student(
                        student_id=row['ID'],
                        name=row['Name'],
                        email=email
                    )
            st.success("Changes saved!")
            st.rerun()

        st.markdown("---")

        # Delete student section
        st.subheader("🗑️ Remove Student")
        col1, col2 = st.columns([3, 1])

        student_options = {s['name']: s['id'] for s in students}
        with col1:
            selected_student = st.selectbox(
                "Select student to remove",
                options=list(student_options.keys()),
                key="delete_student_select"
            )
        with col2:
            st.write("")
            st.write("")
            if st.button("🗑️ Remove", type="secondary", use_container_width=True):
                st.session_state['confirm_delete_student'] = selected_student

        # Confirmation
        if st.session_state.get('confirm_delete_student'):
            student_to_delete = st.session_state['confirm_delete_student']
            st.error(f"⚠️ Are you sure you want to remove '{student_to_delete}'?")
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("Yes, Remove", type="primary"):
                    student_id = student_options[student_to_delete]
                    db.delete_student(student_id)
                    st.session_state.pop('confirm_delete_student', None)
                    st.success(f"Student '{student_to_delete}' removed.")
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.pop('confirm_delete_student', None)
                    st.rerun()
    else:
        st.info(f"No students in {selected_class_name} yet. Add students above!")
