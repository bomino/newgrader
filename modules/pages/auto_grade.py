import streamlit as st
import pandas as pd
from modules import database as db

def render():
    st.title("🤖 Auto-Grade")

    tab1, tab2 = st.tabs(["📝 Create Answer Key", "🎯 Grade Responses"])

    with tab1:
        render_answer_key_tab()

    with tab2:
        render_grading_tab()


def render_answer_key_tab():
    """Tab for creating/editing answer keys."""
    st.subheader("Create Answer Key")

    # Get all classes and assignments
    classes = db.get_all_classes()
    if not classes:
        st.warning("No classes found. Please create a class first.")
        return

    class_options = {c['name']: c['id'] for c in classes}
    selected_class_name = st.selectbox(
        "Select Class",
        options=list(class_options.keys()),
        key="answer_key_class_select"
    )
    selected_class_id = class_options[selected_class_name]

    assignments = db.get_assignments_by_class(selected_class_id)
    if not assignments:
        st.warning("No assignments found. Please create an assignment first.")
        return

    assignment_options = {f"{a['name']} ({a['max_points']} pts)": a['id'] for a in assignments}
    selected_assignment_key = st.selectbox(
        "Select Assignment",
        options=list(assignment_options.keys()),
        key="answer_key_assignment_select"
    )
    selected_assignment_id = assignment_options[selected_assignment_key]

    st.markdown("---")

    # Load existing answer key
    existing_key = db.get_answer_key(selected_assignment_id)

    # Number of questions
    num_questions = st.number_input(
        "Number of Questions",
        min_value=1,
        max_value=100,
        value=max(len(existing_key), 10) if existing_key else 10,
        step=1
    )

    # Build answer key editor
    if existing_key:
        key_data = []
        for i in range(1, num_questions + 1):
            existing = next((q for q in existing_key if q['question_num'] == i), None)
            key_data.append({
                "Q#": i,
                "Answer": existing['correct_answer'] if existing else "",
                "Points": existing['points'] if existing else 1.0,
                "Type": existing['question_type'] if existing else "multiple_choice"
            })
    else:
        key_data = [{"Q#": i, "Answer": "", "Points": 1.0, "Type": "multiple_choice"} for i in range(1, num_questions + 1)]

    df = pd.DataFrame(key_data)

    st.caption("Enter the correct answer for each question. For multiple choice, use A, B, C, D, etc.")

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        disabled=["Q#"],
        column_config={
            "Q#": st.column_config.NumberColumn("Q#", width="small"),
            "Answer": st.column_config.TextColumn("Correct Answer", width="medium"),
            "Points": st.column_config.NumberColumn("Points", min_value=0.0, max_value=100.0, step=0.5, width="small"),
            "Type": st.column_config.SelectboxColumn(
                "Type",
                options=["multiple_choice", "short_text", "numeric"],
                width="medium"
            )
        },
        key="answer_key_editor"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Answer Key", type="primary", use_container_width=True):
            questions = []
            for idx, row in edited_df.iterrows():
                if row['Answer'].strip():
                    questions.append({
                        'question_num': row['Q#'],
                        'correct_answer': row['Answer'].strip().upper() if row['Type'] == 'multiple_choice' else row['Answer'].strip(),
                        'points': row['Points'],
                        'question_type': row['Type']
                    })

            if questions:
                db.set_answer_key(selected_assignment_id, questions)
                st.success(f"Saved answer key with {len(questions)} questions!")
            else:
                st.warning("No answers to save. Please fill in at least one answer.")

    with col2:
        if st.button("🗑️ Clear Answer Key", use_container_width=True):
            db.delete_answer_key(selected_assignment_id)
            st.success("Answer key cleared!")
            st.rerun()


def render_grading_tab():
    """Tab for auto-grading student responses."""
    st.subheader("Auto-Grade Student Responses")

    # Get all classes and assignments
    classes = db.get_all_classes()
    if not classes:
        st.warning("No classes found. Please create a class first.")
        return

    class_options = {c['name']: c['id'] for c in classes}
    selected_class_name = st.selectbox(
        "Select Class",
        options=list(class_options.keys()),
        key="grading_class_select"
    )
    selected_class_id = class_options[selected_class_name]

    assignments = db.get_assignments_by_class(selected_class_id)
    if not assignments:
        st.warning("No assignments found. Please create an assignment first.")
        return

    assignment_options = {f"{a['name']} ({a['max_points']} pts)": a['id'] for a in assignments}
    selected_assignment_key = st.selectbox(
        "Select Assignment",
        options=list(assignment_options.keys()),
        key="grading_assignment_select"
    )
    selected_assignment_id = assignment_options[selected_assignment_key]
    selected_assignment = db.get_assignment_by_id(selected_assignment_id)

    # Check for answer key
    answer_key = db.get_answer_key(selected_assignment_id)
    if not answer_key:
        st.warning("No answer key found for this assignment. Please create one first.")
        return

    st.success(f"Answer key loaded with {len(answer_key)} questions.")

    st.markdown("---")

    # File upload
    st.subheader("Upload Student Responses")
    st.caption("Upload a CSV or Excel file with columns: student_name, q1, q2, q3, ...")

    uploaded_file = st.file_uploader(
        "Choose file",
        type=['csv', 'xlsx'],
        key="response_file_upload"
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                responses_df = pd.read_csv(uploaded_file)
            else:
                responses_df = pd.read_excel(uploaded_file)

            st.write("Preview of uploaded data:")
            st.dataframe(responses_df.head(), use_container_width=True)

            # Find student name column
            name_col = None
            for col in responses_df.columns:
                if 'name' in col.lower() or 'student' in col.lower():
                    name_col = col
                    break

            if not name_col:
                name_col = responses_df.columns[0]
                st.info(f"Using '{name_col}' as student name column.")

            # Grade the responses
            if st.button("🎯 Grade Responses", type="primary", use_container_width=True):
                results = grade_responses(responses_df, name_col, answer_key, selected_assignment)

                # Store results in session state
                st.session_state['grading_results'] = results
                st.session_state['grading_assignment_id'] = selected_assignment_id
                st.session_state['grading_class_id'] = selected_class_id
                st.rerun()

        except Exception as e:
            st.error(f"Error reading file: {e}")

    # Display grading results if available
    if st.session_state.get('grading_results') and st.session_state.get('grading_assignment_id') == selected_assignment_id:
        display_grading_results()


def grade_responses(responses_df, name_col, answer_key, assignment):
    """Grade student responses against the answer key."""
    results = []

    # Create answer key lookup
    key_lookup = {q['question_num']: q for q in answer_key}

    for idx, row in responses_df.iterrows():
        student_name = str(row[name_col]).strip()
        total_points = 0
        max_points = 0
        details = []

        for q_num, q_data in key_lookup.items():
            col_name = f"q{q_num}"
            # Try different column naming conventions
            student_answer = None
            for possible_col in [col_name, f"Q{q_num}", f"question{q_num}", f"Question {q_num}"]:
                if possible_col in row.index:
                    student_answer = str(row[possible_col]).strip().upper() if pd.notna(row[possible_col]) else ""
                    break

            if student_answer is None:
                # Try numeric column index
                try:
                    student_answer = str(row.iloc[q_num]).strip().upper() if pd.notna(row.iloc[q_num]) else ""
                except:
                    student_answer = ""

            correct_answer = q_data['correct_answer'].upper()
            points = q_data['points']
            max_points += points

            # Check answer based on type
            is_correct = False
            if q_data['question_type'] == 'multiple_choice':
                is_correct = student_answer == correct_answer
            elif q_data['question_type'] == 'short_text':
                is_correct = student_answer.lower() == correct_answer.lower()
            elif q_data['question_type'] == 'numeric':
                try:
                    is_correct = abs(float(student_answer) - float(correct_answer)) < 0.01
                except:
                    is_correct = False

            if is_correct:
                total_points += points

            details.append({
                'question': q_num,
                'student_answer': student_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'points_earned': points if is_correct else 0,
                'points_possible': points
            })

        # Scale to assignment max points
        if max_points > 0:
            scaled_score = (total_points / max_points) * assignment['max_points']
        else:
            scaled_score = 0

        results.append({
            'student_name': student_name,
            'raw_score': total_points,
            'max_raw': max_points,
            'scaled_score': round(scaled_score, 2),
            'percentage': round((total_points / max_points) * 100, 1) if max_points > 0 else 0,
            'details': details
        })

    return results


def display_grading_results():
    """Display grading results with option to save."""
    results = st.session_state['grading_results']
    assignment_id = st.session_state['grading_assignment_id']
    class_id = st.session_state['grading_class_id']

    st.markdown("---")
    st.subheader("📊 Grading Results")

    # Summary table
    summary_data = []
    for r in results:
        summary_data.append({
            "Student": r['student_name'],
            "Score": r['scaled_score'],
            "Percentage": f"{r['percentage']}%",
            "Correct": f"{sum(1 for d in r['details'] if d['is_correct'])}/{len(r['details'])}"
        })

    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    scores = [r['scaled_score'] for r in results]
    with col1:
        st.metric("Average", f"{sum(scores)/len(scores):.1f}")
    with col2:
        st.metric("Highest", f"{max(scores):.1f}")
    with col3:
        st.metric("Lowest", f"{min(scores):.1f}")
    with col4:
        passing = sum(1 for r in results if r['percentage'] >= 60)
        st.metric("Passing (60%+)", f"{passing}/{len(results)}")

    # Save to database
    st.markdown("---")
    if st.button("💾 Save Grades to Database", type="primary", use_container_width=True):
        # Get students from class
        students = db.get_students_by_class(class_id)
        student_lookup = {s['name'].lower(): s['id'] for s in students}

        saved_count = 0
        not_found = []

        for r in results:
            student_id = student_lookup.get(r['student_name'].lower())
            if student_id:
                db.set_grade(student_id, assignment_id, r['scaled_score'])
                saved_count += 1
            else:
                not_found.append(r['student_name'])

        if saved_count > 0:
            st.success(f"Saved {saved_count} grades to database!")

        if not_found:
            st.warning(f"Could not find students: {', '.join(not_found)}")

    # Detailed breakdown expander
    with st.expander("📋 Detailed Question Breakdown"):
        for r in results:
            st.write(f"**{r['student_name']}** - {r['scaled_score']} pts ({r['percentage']}%)")
            details_df = pd.DataFrame(r['details'])
            details_df['Result'] = details_df['is_correct'].apply(lambda x: '✓' if x else '✗')
            st.dataframe(
                details_df[['question', 'student_answer', 'correct_answer', 'Result', 'points_earned']],
                use_container_width=True,
                hide_index=True
            )
            st.markdown("---")
