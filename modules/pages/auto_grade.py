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
        <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700;">Auto-Grade</h1>
        <p style="margin: 0.25rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">Create answer keys and auto-grade student responses</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Create Answer Key", "Grade Responses"])

    with tab1:
        render_answer_key_tab()

    with tab2:
        render_grading_tab()


def render_answer_key_tab():
    """Tab for creating/editing answer keys."""

    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    ">
        <h3 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">Create Answer Key</h3>
        <p style="color: #718096; font-size: 0.85rem; margin: 0;">Define correct answers for automatic grading.</p>
    </div>
    """, unsafe_allow_html=True)

    # Get all classes and assignments
    classes = db.get_all_classes()
    if not classes:
        st.warning("No classes found. Please create a class first.")
        return

    col1, col2 = st.columns(2)

    with col1:
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

    with col2:
        assignment_options = {f"{a['name']} ({a['max_points']} pts)": a['id'] for a in assignments}
        selected_assignment_key = st.selectbox(
            "Select Assignment",
            options=list(assignment_options.keys()),
            key="answer_key_assignment_select"
        )
        selected_assignment_id = assignment_options[selected_assignment_key]

    # Load existing answer key
    existing_key = db.get_answer_key(selected_assignment_id)

    # Status indicator
    if existing_key:
        st.markdown(f"""
        <div style="
            background: #f0fff4;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid #38a169;
            margin: 1rem 0;
        ">
            <span style="color: #38a169; font-weight: 500;">Answer key exists with {len(existing_key)} questions</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: #fffaf0;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid #d69e2e;
            margin: 1rem 0;
        ">
            <span style="color: #d69e2e; font-weight: 500;">No answer key yet. Create one below.</span>
        </div>
        """, unsafe_allow_html=True)

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
        if st.button("Save Answer Key", type="primary", use_container_width=True):
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
        if st.button("Clear Answer Key", use_container_width=True):
            db.delete_answer_key(selected_assignment_id)
            st.success("Answer key cleared!")
            st.rerun()


def render_grading_tab():
    """Tab for auto-grading student responses."""

    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    ">
        <h3 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">Auto-Grade Student Responses</h3>
        <p style="color: #718096; font-size: 0.85rem; margin: 0;">Upload student responses to grade automatically.</p>
    </div>
    """, unsafe_allow_html=True)

    # Get all classes and assignments
    classes = db.get_all_classes()
    if not classes:
        st.warning("No classes found. Please create a class first.")
        return

    col1, col2 = st.columns(2)

    with col1:
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

    with col2:
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
        st.markdown("""
        <div style="
            background: #fff5f5;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e53e3e;
            margin: 1rem 0;
        ">
            <span style="color: #e53e3e; font-weight: 500;">No answer key found. Please create one in the "Create Answer Key" tab first.</span>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div style="
        background: #f0fff4;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: 1px solid #38a169;
        margin: 1rem 0;
    ">
        <span style="color: #38a169; font-weight: 500;">Answer key loaded with {len(answer_key)} questions</span>
    </div>
    """, unsafe_allow_html=True)

    # File upload section
    st.markdown("""
    <div style="
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #1e3a5f; font-size: 1rem;">Upload Student Responses</h4>
        <p style="color: #718096; font-size: 0.85rem; margin: 0;">
            Upload a CSV or Excel file with columns: <code>student_name, q1, q2, q3, ...</code>
        </p>
    </div>
    """, unsafe_allow_html=True)

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

            st.markdown("""
            <div style="
                background: #ebf8ff;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                border: 1px solid #3182ce;
                margin-bottom: 0.5rem;
            ">
                <span style="color: #3182ce; font-weight: 600;">Preview of uploaded data</span>
            </div>
            """, unsafe_allow_html=True)
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
            if st.button("Grade Responses", type="primary", use_container_width=True):
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

    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 1.5rem 0 1rem 0;
    ">
        <h3 style="margin: 0; color: #1e3a5f; font-size: 1.1rem;">Grading Results</h3>
    </div>
    """, unsafe_allow_html=True)

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

    # Statistics cards
    scores = [r['scaled_score'] for r in results]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="
            background: #38a169;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 1.75rem; font-weight: 700;">{sum(scores)/len(scores):.1f}</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Average</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background: #3182ce;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 1.75rem; font-weight: 700;">{max(scores):.1f}</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Highest</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background: #e53e3e;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 1.75rem; font-weight: 700;">{min(scores):.1f}</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Lowest</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        passing = sum(1 for r in results if r['percentage'] >= 60)
        st.markdown(f"""
        <div style="
            background: #d69e2e;
            color: white;
            padding: 1.25rem;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 1.75rem; font-weight: 700;">{passing}/{len(results)}</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Passing (60%+)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Save to database
    if st.button("Save Grades to Database", type="primary", use_container_width=True):
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
    with st.expander("Detailed Question Breakdown"):
        for r in results:
            st.markdown(f"""
            <div style="
                background: #f7fafc;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                margin-bottom: 0.5rem;
                border-left: 4px solid #1e3a5f;
            ">
                <strong>{r['student_name']}</strong> - {r['scaled_score']} pts ({r['percentage']}%)
            </div>
            """, unsafe_allow_html=True)
            details_df = pd.DataFrame(r['details'])
            details_df['Result'] = details_df['is_correct'].apply(lambda x: 'Correct' if x else 'Incorrect')
            st.dataframe(
                details_df[['question', 'student_answer', 'correct_answer', 'Result', 'points_earned']],
                use_container_width=True,
                hide_index=True
            )
            st.markdown("---")
