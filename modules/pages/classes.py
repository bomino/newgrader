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
        <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700;">Class Management</h1>
        <p style="margin: 0.25rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">Create and organize your classes</p>
    </div>
    """, unsafe_allow_html=True)

    # Add new class card
    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    ">
        <h3 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">Add New Class</h3>
        <p style="color: #718096; font-size: 0.85rem; margin: 0;">Create a new class to get started.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_class_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_class_name = st.text_input(
                "Class Name",
                placeholder="e.g., Math 101, English 9A, Physics AP",
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Add Class", use_container_width=True, type="primary")

        if submitted:
            if new_class_name.strip():
                try:
                    db.add_class(new_class_name.strip())
                    st.success(f"Class '{new_class_name}' created successfully!")
                    st.rerun()
                except Exception as e:
                    if "UNIQUE constraint" in str(e):
                        st.error("A class with this name already exists.")
                    else:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter a class name.")

    # Display all classes
    classes = db.get_all_classes()

    if classes:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0; color: #1e3a5f; font-size: 1rem;">
                Your Classes ({len(classes)})
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Class cards grid
        cols = st.columns(3)
        for i, c in enumerate(classes):
            student_count = db.get_student_count_by_class(c['id'])
            assignment_count = len(db.get_assignments_by_class(c['id']))

            with cols[i % 3]:
                st.markdown(f"""
                <div style="
                    background-color: #1e3a5f;
                    color: white;
                    padding: 1.25rem;
                    border-radius: 8px;
                    margin-bottom: 1rem;
                ">
                    <h4 style="margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 600;">{c['name']}</h4>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        {student_count} students | {assignment_count} assignments
                    </div>
                    <div style="margin-top: 0.5rem; font-size: 0.75rem; opacity: 0.7;">
                        Created: {c['created_at'][:10] if c['created_at'] else 'N/A'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Delete class section
        st.markdown("""
        <div style="
            background: #fff5f5;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #fed7d7;
        ">
            <h3 style="margin: 0 0 0.5rem 0; color: #c53030; font-size: 1rem;">Delete a Class</h3>
            <p style="color: #c53030; font-size: 0.85rem; margin: 0;">
                Warning: This will delete all students, assignments, and grades in this class.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            class_options = {c['name']: c['id'] for c in classes}
            selected_class = st.selectbox(
                "Select class to delete",
                options=list(class_options.keys()),
                key="delete_class_select",
                label_visibility="collapsed"
            )
        with col2:
            if st.button("Delete", type="secondary", use_container_width=True):
                st.session_state['confirm_delete'] = selected_class

        if st.session_state.get('confirm_delete'):
            class_to_delete = st.session_state['confirm_delete']
            st.error(f"Are you sure you want to delete '{class_to_delete}'? This cannot be undone.")
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("Yes, Delete", type="primary"):
                    class_id = class_options[class_to_delete]
                    db.delete_class(class_id)
                    st.session_state.pop('confirm_delete', None)
                    st.success(f"Class '{class_to_delete}' deleted.")
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.pop('confirm_delete', None)
                    st.rerun()
    else:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 4rem 2rem;
            background: white;
            border-radius: 8px;
            border: 2px dashed #e2e8f0;
        ">
            <h3 style="color: #1e3a5f; margin-bottom: 0.5rem;">No Classes Yet</h3>
            <p style="color: #718096;">Create your first class to get started!</p>
        </div>
        """, unsafe_allow_html=True)
