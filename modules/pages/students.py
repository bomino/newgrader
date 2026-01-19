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
        <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700;">Student Roster</h1>
        <p style="margin: 0.25rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">Manage students in your classes</p>
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
            <p style="color: #718096;">Create a class first to add students.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Class selector
    st.markdown("""
    <div style="
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    ">
        <label style="color: #1e3a5f; font-weight: 600; font-size: 0.9rem;">Select Class</label>
    </div>
    """, unsafe_allow_html=True)

    class_options = {c['name']: c['id'] for c in classes}
    selected_class_name = st.selectbox(
        "Select Class",
        options=list(class_options.keys()),
        key="student_class_select",
        label_visibility="collapsed"
    )
    selected_class_id = class_options[selected_class_name]

    # Two columns: Add student form and bulk import
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">Add Student</h3>
            <p style="color: #718096; font-size: 0.85rem; margin: 0;">Add a single student to the class.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("add_student_form", clear_on_submit=True):
            student_name = st.text_input("Student Name", placeholder="e.g., John Smith")
            student_email = st.text_input("Email (optional)", placeholder="e.g., john@school.edu")
            submitted = st.form_submit_button("Add Student", use_container_width=True, type="primary")

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
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">Bulk Import</h3>
            <p style="color: #718096; font-size: 0.85rem; margin: 0;">Import multiple students from a CSV file.</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="CSV should have columns: name (required), email (optional)"
        )

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.caption(f"Preview ({len(df)} students)")
                st.dataframe(df.head(5), use_container_width=True, hide_index=True)

                if st.button("Import All Students", use_container_width=True, type="primary"):
                    students = df.to_dict('records')
                    added = db.bulk_add_students(students, selected_class_id)
                    st.success(f"Imported {added} students!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

    # Display students in selected class
    students = db.get_students_by_class(selected_class_id)

    if students:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin: 1.5rem 0 1rem 0;
        ">
            <h3 style="margin: 0; color: #1e3a5f; font-size: 1rem;">
                Students in {selected_class_name}
                <span style="
                    background: #1e3a5f;
                    color: white;
                    padding: 0.25rem 0.75rem;
                    border-radius: 4px;
                    font-size: 0.8rem;
                    margin-left: 0.5rem;
                ">{len(students)}</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Create dataframe for display
        df = pd.DataFrame(students)
        df = df[['id', 'name', 'email', 'created_at']]
        df.columns = ['ID', 'Name', 'Email', 'Added']
        df['Added'] = df['Added'].apply(lambda x: x[:10] if x else 'N/A')
        df['Email'] = df['Email'].fillna('-')

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

        if st.button("Save Changes", use_container_width=True, type="primary"):
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
        st.markdown("""
        <div style="
            background: #fff5f5;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #fed7d7;
        ">
            <h3 style="margin: 0 0 0.5rem 0; color: #c53030; font-size: 1rem;">Remove Student</h3>
            <p style="color: #c53030; font-size: 0.85rem; margin: 0;">
                This will permanently remove the student and their grades.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        student_options = {s['name']: s['id'] for s in students}
        with col1:
            selected_student = st.selectbox(
                "Select student to remove",
                options=list(student_options.keys()),
                key="delete_student_select",
                label_visibility="collapsed"
            )
        with col2:
            if st.button("Remove", type="secondary", use_container_width=True):
                st.session_state['confirm_delete_student'] = selected_student

        if st.session_state.get('confirm_delete_student'):
            student_to_delete = st.session_state['confirm_delete_student']
            st.error(f"Are you sure you want to remove '{student_to_delete}'?")
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
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 4rem 2rem;
            background: white;
            border-radius: 8px;
            border: 2px dashed #e2e8f0;
            margin-top: 1.5rem;
        ">
            <h3 style="color: #1e3a5f; margin-bottom: 0.5rem;">No Students Yet</h3>
            <p style="color: #718096;">Add students to {selected_class_name} using the forms above.</p>
        </div>
        """, unsafe_allow_html=True)
