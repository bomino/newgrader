import streamlit as st
import pandas as pd
from datetime import date
from modules import database as db

def render():
    st.title("📝 Assignment Management")

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
        key="assignment_class_select"
    )
    selected_class_id = class_options[selected_class_name]

    st.markdown("---")

    # Add new assignment form
    with st.expander("➕ Add New Assignment", expanded=False):
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

            submitted = st.form_submit_button("Add Assignment", use_container_width=True)

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

    st.markdown("---")

    # Display assignments for selected class
    assignments = db.get_assignments_by_class(selected_class_id)

    if assignments:
        st.subheader(f"Assignments for {selected_class_name} ({len(assignments)})")

        # Create dataframe for display
        data = []
        for a in assignments:
            data.append({
                "ID": a['id'],
                "Name": a['name'],
                "Max Points": a['max_points'],
                "Weight": a['weight'],
                "Due Date": a['due_date'] if a['due_date'] else "-",
            })

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Name": st.column_config.TextColumn("Name", width="large"),
                "Max Points": st.column_config.NumberColumn("Max Points", width="small"),
                "Weight": st.column_config.NumberColumn("Weight", width="small"),
                "Due Date": st.column_config.TextColumn("Due Date", width="medium"),
            }
        )

        st.markdown("---")

        # Edit assignment section
        st.subheader("✏️ Edit Assignment")
        assignment_options = {f"{a['name']} (ID: {a['id']})": a['id'] for a in assignments}

        selected_assignment_key = st.selectbox(
            "Select assignment to edit",
            options=list(assignment_options.keys()),
            key="edit_assignment_select"
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
                    update_btn = st.form_submit_button("💾 Save Changes", use_container_width=True)
                with col2:
                    delete_btn = st.form_submit_button("🗑️ Delete Assignment", use_container_width=True)

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

        # Confirmation dialog for delete
        if st.session_state.get('confirm_delete_assignment'):
            st.error("⚠️ Are you sure you want to delete this assignment? This will also delete all associated grades.")
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
        st.info(f"No assignments for {selected_class_name} yet. Add one above!")
