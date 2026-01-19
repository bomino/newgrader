# NewGrader - Teacher Grading Application

## Project Overview

A Streamlit-based grading application for teachers to manage students, assignments, and grades with auto-grading capabilities.

**Documentation:** See `docs/USER_GUIDE.md` for comprehensive user documentation.

## Tech Stack

- **Python 3.8+** - Core language
- **Streamlit** - Web UI framework
- **SQLite** - Embedded database
- **Pandas** - Data manipulation and display
- **openpyxl** - Excel file generation

## Project Structure

```
NewGrader/
├── app.py                    # Main entry point, routing
├── requirements.txt          # Python dependencies
├── CLAUDE.md                 # Technical documentation (this file)
├── .gitignore               # Git ignore rules
│
├── data/
│   └── grader.db            # SQLite database (auto-created)
│
├── docs/
│   └── USER_GUIDE.md        # User documentation
│
├── modules/
│   ├── __init__.py
│   ├── database.py          # All database operations
│   └── pages/
│       ├── __init__.py
│       ├── classes.py       # Class management UI
│       ├── students.py      # Student roster UI
│       ├── assignments.py   # Assignment management UI
│       ├── grade_entry.py   # Manual grade entry UI
│       ├── auto_grade.py    # Answer keys & auto-grading UI
│       ├── gradebook.py     # Gradebook view & exports
│       └── settings.py      # Grade scale configuration
│
├── venv/                    # Virtual environment (not in git)
│
└── scripts/ralph/           # Ralph autonomous agent files
    ├── prd.json
    ├── prompt-claude.md
    ├── ralph-claude.ps1
    └── ralph-claude.sh
```

## Development Commands

```bash
# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (cmd)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Run on specific port
streamlit run app.py --server.port 8080
```

## Database Schema

### Tables

```sql
-- Classes table
CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    class_id INTEGER NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
);

-- Assignments table
CREATE TABLE assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    class_id INTEGER NOT NULL,
    max_points REAL NOT NULL DEFAULT 100,
    weight REAL NOT NULL DEFAULT 1.0,
    due_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
);

-- Grades table
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    assignment_id INTEGER NOT NULL,
    points REAL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE,
    UNIQUE(student_id, assignment_id)
);

-- Answer keys table
CREATE TABLE answer_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER NOT NULL,
    question_num INTEGER NOT NULL,
    correct_answer TEXT NOT NULL,
    points REAL NOT NULL DEFAULT 1.0,
    question_type TEXT DEFAULT 'multiple_choice',
    FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE,
    UNIQUE(assignment_id, question_num)
);

-- Settings table
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

### Relationships

```
classes (1) ──────< (many) students
classes (1) ──────< (many) assignments
assignments (1) ──< (many) grades
assignments (1) ──< (many) answer_keys
students (1) ─────< (many) grades
```

## Architecture

### Page Module Pattern

Each page module follows this pattern:

```python
# modules/pages/example.py
import streamlit as st
from modules import database as db

def render():
    st.title("Page Title")
    # Page logic here
```

### Database Module

All database operations are centralized in `modules/database.py`:

```python
# Connection management
get_connection()      # Context manager for DB connections
init_db()            # Initialize tables on startup

# CRUD Operations (per entity)
get_all_*()          # List all records
get_*_by_id(id)      # Get single record
add_*(...)           # Create new record
update_*(id, ...)    # Update existing record
delete_*(id)         # Delete record

# Special operations
bulk_add_students()  # Bulk insert
bulk_set_grades()    # Upsert grades
get_grade_scale()    # Get JSON settings
set_grade_scale()    # Save JSON settings
```

### State Management

Use `st.session_state` for:
- Confirmation dialogs (`st.session_state['confirm_delete']`)
- Grading results (`st.session_state['grading_results']`)
- Cross-page navigation hints

## Conventions

### Code Style

- Use `st.session_state` for maintaining state between reruns
- All database operations go through `modules/database.py`
- Pages use Streamlit's native components (`st.dataframe`, `st.form`, etc.)
- Error handling: use `st.error()` and `st.success()` for user feedback

### UI Patterns

- Use `st.form()` for data entry to prevent rerun on each input
- Use `st.expander()` for collapsible sections
- Use `st.columns()` for side-by-side layouts
- Use `st.data_editor()` for editable tables

### Database Patterns

- Always use context manager: `with get_connection() as conn:`
- Return `dict(row)` for single records, `[dict(row) for row in rows]` for lists
- Use `ON CONFLICT ... DO UPDATE` for upserts

## Key Algorithms

### Weighted Average Calculation

```python
# In gradebook.py
total_weighted = 0
total_weight = 0

for assignment in assignments:
    grade = get_grade(student_id, assignment['id'])
    if grade and grade['points'] is not None:
        percentage = (grade['points'] / assignment['max_points']) * 100
        total_weighted += percentage * assignment['weight']
        total_weight += assignment['weight']

weighted_average = total_weighted / total_weight if total_weight > 0 else 0
```

### Auto-Grading Logic

```python
# In auto_grade.py
for question in answer_key:
    student_answer = get_student_answer(row, question['question_num'])
    correct_answer = question['correct_answer']

    if question['question_type'] == 'multiple_choice':
        is_correct = student_answer.upper() == correct_answer.upper()
    elif question['question_type'] == 'short_text':
        is_correct = student_answer.lower() == correct_answer.lower()
    elif question['question_type'] == 'numeric':
        is_correct = abs(float(student_answer) - float(correct_answer)) < 0.01

    if is_correct:
        score += question['points']
```

### Letter Grade Conversion

```python
def get_letter_grade(percentage, scale):
    if percentage >= scale['A']: return 'A'
    elif percentage >= scale['B']: return 'B'
    elif percentage >= scale['C']: return 'C'
    elif percentage >= scale['D']: return 'D'
    else: return 'F'
```

## Adding New Features

### Adding a New Page

1. Create `modules/pages/newpage.py` with a `render()` function
2. Import in `app.py`: `from modules.pages import newpage`
3. Add to `PAGES` dict and routing `elif` block

### Adding a New Database Table

1. Add `CREATE TABLE` in `init_db()` in `database.py`
2. Add CRUD functions following existing patterns
3. Delete `data/grader.db` to recreate schema (or use migrations)

### Adding New Settings

1. Use `get_setting(key, default)` and `set_setting(key, value)`
2. Settings are stored as strings; use JSON for complex values

## Testing Manually

1. Create a class: "Test Class"
2. Add 3-5 students
3. Create an assignment: "Quiz 1", 10 points
4. Create answer key: 5 questions, A/B/C/D/A
5. Upload test CSV with responses
6. Verify grades appear in gradebook
7. Export to Excel and verify file

## Known Limitations

- Single-user application (no authentication)
- SQLite limits concurrent writes
- Large file uploads may be slow
- No undo functionality (use exports for backup)
