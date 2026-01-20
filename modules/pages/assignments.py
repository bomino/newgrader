import streamlit as st
import pandas as pd
from datetime import date
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
        <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700; color: white;">Assignment Management</h1>
        <p style="margin: 0.25rem 0 0 0; opacity: 0.9; font-size: 0.95rem; color: white;">Create and manage assignments for your classes</p>
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
            <p style="color: #718096;">Create a class first to add assignments.</p>
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
        key="assignment_class_select",
        label_visibility="collapsed"
    )
    selected_class_id = class_options[selected_class_name]

    # Add new assignment
    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    ">
        <h3 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">Add New Assignment</h3>
        <p style="color: #718096; font-size: 0.85rem; margin: 0;">Create a new assignment with points and weight.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Create Assignment", expanded=False):
        with st.form("add_assignment_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                assignment_name = st.text_input(
                    "Assignment Name",
                    placeholder="e.g., Chapter 1 Quiz, Midterm Exam"
                )
                max_points = st.number_input(
                    "Max Points",
                    min_value=1.0,
                    max_value=1000.0,
                    value=100.0,
                    step=1.0
                )

            with col2:
                weight = st.number_input(
                    "Weight",
                    min_value=0.1,
                    max_value=10.0,
                    value=1.0,
                    step=0.1,
                    help="Weight for grade calculation (e.g., 2.0 = counts double)"
                )
                due_date = st.date_input(
                    "Due Date (optional)",
                    value=None,
                    min_value=date(2020, 1, 1)
                )

            submitted = st.form_submit_button("Add Assignment", use_container_width=True, type="primary")

            if submitted:
                if assignment_name.strip():
                    due_date_str = due_date.isoformat() if due_date else None
                    db.add_assignment(
                        name=assignment_name.strip(),
                        class_id=selected_class_id,
                        max_points=max_points,
                        weight=weight,
                        due_date=due_date_str
                    )
                    st.success(f"Assignment '{assignment_name}' added!")
                    st.rerun()
                else:
                    st.warning("Please enter an assignment name.")

    # Display assignments
    assignments = db.get_assignments_by_class(selected_class_id)

    if assignments:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin: 1rem 0;
        ">
            <h3 style="margin: 0; color: #1e3a5f; font-size: 1rem;">
                Assignments for {selected_class_name}
                <span style="
                    background: #1e3a5f;
                    color: white;
                    padding: 0.25rem 0.75rem;
                    border-radius: 4px;
                    font-size: 0.8rem;
                    margin-left: 0.5rem;
                ">{len(assignments)}</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Assignment cards
        cols = st.columns(3)
        for i, a in enumerate(assignments):
            due_text = a['due_date'] if a['due_date'] else "No due date"

            with cols[i % 3]:
                st.markdown(f"""
                <div style="
                    background-color: #1e3a5f;
                    color: white;
                    padding: 1.25rem;
                    border-radius: 8px;
                    margin-bottom: 1rem;
                ">
                    <h4 style="margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 600; color: white;">{a['name']}</h4>
                    <div style="font-size: 0.85rem; opacity: 0.9; color: white;">
                        {a['max_points']} pts | Weight: {a['weight']}
                    </div>
                    <div style="margin-top: 0.5rem; font-size: 0.75rem; opacity: 0.7; color: white;">
                        Due: {due_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Edit assignment section
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">Edit Assignment</h3>
            <p style="color: #718096; font-size: 0.85rem; margin: 0;">Modify or delete an existing assignment.</p>
        </div>
        """, unsafe_allow_html=True)

        assignment_options = {f"{a['name']} ({a['max_points']} pts)": a['id'] for a in assignments}

        selected_assignment_key = st.selectbox(
            "Select assignment to edit",
            options=list(assignment_options.keys()),
            key="edit_assignment_select",
            label_visibility="collapsed"
        )
        selected_assignment_id = assignment_options[selected_assignment_key]
        selected_assignment = db.get_assignment_by_id(selected_assignment_id)

        if selected_assignment:
            with st.form("edit_assignment_form"):
                col1, col2 = st.columns(2)

                with col1:
                    edit_name = st.text_input(
                        "Assignment Name",
                        value=selected_assignment['name']
                    )
                    edit_max_points = st.number_input(
                        "Max Points",
                        min_value=1.0,
                        max_value=1000.0,
                        value=float(selected_assignment['max_points']),
                        step=1.0
                    )

                with col2:
                    edit_weight = st.number_input(
                        "Weight",
                        min_value=0.1,
                        max_value=10.0,
                        value=float(selected_assignment['weight']),
                        step=0.1
                    )
                    current_due = None
                    if selected_assignment['due_date']:
                        try:
                            current_due = date.fromisoformat(selected_assignment['due_date'])
                        except:
                            pass
                    edit_due_date = st.date_input(
                        "Due Date",
                        value=current_due,
                        min_value=date(2020, 1, 1)
                    )

                col1, col2 = st.columns(2)
                with col1:
                    update_btn = st.form_submit_button("Save Changes", use_container_width=True, type="primary")
                with col2:
                    delete_btn = st.form_submit_button("Delete Assignment", use_container_width=True)

                if update_btn:
                    due_date_str = edit_due_date.isoformat() if edit_due_date else None
                    db.update_assignment(
                        assignment_id=selected_assignment_id,
                        name=edit_name,
                        max_points=edit_max_points,
                        weight=edit_weight,
                        due_date=due_date_str
                    )
                    st.success("Assignment updated!")
                    st.rerun()

                if delete_btn:
                    st.session_state['confirm_delete_assignment'] = selected_assignment_id

        if st.session_state.get('confirm_delete_assignment'):
            st.error("Are you sure you want to delete this assignment? This will also delete all associated grades.")
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("Yes, Delete", type="primary"):
                    db.delete_assignment(st.session_state['confirm_delete_assignment'])
                    st.session_state.pop('confirm_delete_assignment', None)
                    st.success("Assignment deleted!")
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.pop('confirm_delete_assignment', None)
                    st.rerun()
    else:
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 4rem 2rem;
            background: white;
            border-radius: 8px;
            border: 2px dashed #e2e8f0;
            margin-top: 1rem;
        ">
            <h3 style="color: #1e3a5f; margin-bottom: 0.5rem;">No Assignments Yet</h3>
            <p style="color: #718096;">Create your first assignment for {selected_class_name}!</p>
        </div>
        """, unsafe_allow_html=True)
