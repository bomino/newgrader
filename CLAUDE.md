# NewGrader - Teacher Grading Application

## Project Overview
A Streamlit-based grading application for teachers to manage students, assignments, and grades with auto-grading capabilities.

## Tech Stack
- Python 3.x
- Streamlit (UI framework)
- SQLite (database)
- Pandas (data manipulation)
- openpyxl (Excel export)

## Project Structure
```
NewGrader/
├── app.py              # Main Streamlit app entry point
├── requirements.txt    # Python dependencies
├── CLAUDE.md          # This file
├── data/
│   └── grader.db      # SQLite database
├── modules/
│   ├── database.py    # Database connection and helpers
│   └── pages/         # Streamlit page modules
└── scripts/
    └── ralph/         # Ralph autonomous agent files
```

## Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Database Schema
- `classes`: id, name
- `students`: id, name, class_id (FK)
- `assignments`: id, name, class_id (FK), max_points, weight, due_date
- `grades`: id, student_id (FK), assignment_id (FK), points, comments
- `answer_keys`: id, assignment_id (FK), question_num, correct_answer, points
- `settings`: key, value (for grade scale config)

## Conventions
- Use st.session_state for maintaining state between reruns
- All database operations go through modules/database.py
- Pages use Streamlit's native components (st.dataframe, st.form, etc.)
- Error handling: use st.error() and st.success() for user feedback
