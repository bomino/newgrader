import streamlit as st
import pandas as pd
from modules import database as db

def render():
    st.title("📋 Class Management")

    # Add new class form
    with st.expander("➕ Add New Class", expanded=False):
        with st.form("add_class_form", clear_on_submit=True):
            new_class_name = st.text_input("Class Name", placeholder="e.g., Math 101, English 9A")
            submitted = st.form_submit_button("Add Class", use_container_width=True)

            if submitted:
                if new_class_name.strip():
                    try:
                        db.add_class(new_class_name.strip())
                        st.success(f"Class '{new_class_name}' added successfully!")
                        st.rerun()
                    except Exception as e:
                        if "UNIQUE constraint" in str(e):
                            st.error("A class with this name already exists.")
                        else:
                            st.error(f"Error adding class: {e}")
                else:
                    st.warning("Please enter a class name.")

    st.markdown("---")

    # Display all classes
    classes = db.get_all_classes()

    if classes:
        st.subheader(f"Your Classes ({len(classes)})")

        # Create a dataframe for display
        class_data = []
        for c in classes:
            student_count = db.get_student_count_by_class(c['id'])
            class_data.append({
                "ID": c['id'],
                "Class Name": c['name'],
                "Students": student_count,
                "Created": c['created_at'][:10] if c['created_at'] else "N/A"
            })

        df = pd.DataFrame(class_data)

        # Display as table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Class Name": st.column_config.TextColumn("Class Name", width="large"),
                "Students": st.column_config.NumberColumn("Students", width="small"),
                "Created": st.column_config.TextColumn("Created", width="medium")
            }
        )

        st.markdown("---")

        # Delete class section
        st.subheader("🗑️ Delete a Class")
        st.warning("Deleting a class will also delete all students in that class.")

        col1, col2 = st.columns([3, 1])
        with col1:
            class_options = {c['name']: c['id'] for c in classes}
            selected_class = st.selectbox(
                "Select class to delete",
                options=list(class_options.keys()),
                key="delete_class_select"
            )
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("🗑️ Delete", type="secondary", use_container_width=True):
                st.session_state['confirm_delete'] = selected_class

        # Confirmation dialog
        if st.session_state.get('confirm_delete'):
            class_to_delete = st.session_state['confirm_delete']
            st.error(f"⚠️ Are you sure you want to delete '{class_to_delete}'?")
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
        st.info("No classes yet. Add your first class above!")
