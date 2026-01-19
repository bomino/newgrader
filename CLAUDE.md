# NewGrader - Technical Documentation

## Project Overview

A Streamlit-based grading application for teachers to manage students, assignments, and grades with auto-grading capabilities.

**Repository:** https://github.com/bomino/newgrader

## Tech Stack

- **Python 3.8+** - Core language
- **Streamlit** - Web UI framework
- **SQLite** - Embedded database
- **Pandas** - Data manipulation and display
- **openpyxl** - Excel file generation
- **Playwright** - UI testing

## Project Structure

```
NewGrader/
├── app.py                    # Main entry point, routing, home dashboard
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest configuration
├── README.md                # User documentation
├── CLAUDE.md                # Technical documentation (this file)
├── .gitignore               # Git ignore rules
│
├── data/
│   └── grader.db            # SQLite database (auto-created)
│
├── modules/
│   ├── __init__.py
│   ├── database.py          # All database operations
│   ├── styles.py            # CSS theming (Navy Blue & White)
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
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_sidebar.py      # Sidebar visibility tests
│   └── screenshots/         # Test screenshots
│
└── venv/                    # Virtual environment (not in git)
```

## Development Commands

```bash
# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (cmd)
venv\Scripts\activate.bat

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Run on specific port
streamlit run app.py --server.port 8080

# Run tests (start app first on port 8502)
streamlit run app.py --server.port 8502 --server.headless true &
pytest tests/ -v
```

## UI Theming

### Color Palette

The application uses a professional Navy Blue & White theme defined in `modules/styles.py`:

```python
COLORS = {
    "primary": "#1e3a5f",        # Navy Blue
    "primary_dark": "#0f2744",   # Dark Navy
    "primary_light": "#2c5282",  # Light Navy
    "secondary": "#3182ce",      # Accent Blue
    "white": "#ffffff",
    "light_gray": "#f7fafc",     # Light Gray (backgrounds)
    "gray": "#718096",           # Medium Gray
    "dark_gray": "#2d3748",      # Dark Gray (text)
    "border": "#e2e8f0",         # Border Gray
    "success": "#38a169",        # Green
    "warning": "#d69e2e",        # Amber/Gold
    "danger": "#e53e3e",         # Red
}
```

### Styling Module

`modules/styles.py` provides:
- `apply_custom_css()` - Applies global CSS styles
- `get_page_header_style()` - Standard page header styling
- `get_card_style()` - Standard card styling
- `get_stat_card_style(variant)` - Stat card styling by variant

### CSS Features

- Navy Blue sidebar with white text
- Prominent expand/collapse button (32x48px)
- Consistent page headers
- Styled form inputs and buttons
- Responsive design

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
    # Page header with Navy Blue styling
    st.markdown("""
    <div style="
        background-color: #1e3a5f;
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    ">
        <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700;">Page Title</h1>
        <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">Page description</p>
    </div>
    """, unsafe_allow_html=True)

    # Page content here
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
bulk_add_students()  # Bulk insert from CSV
bulk_set_grades()    # Upsert multiple grades
get_grade_scale()    # Get JSON settings
set_grade_scale()    # Save JSON settings
get_total_counts()   # Dashboard statistics
```

### State Management

Use `st.session_state` for:
- Confirmation dialogs (`st.session_state['confirm_delete']`)
- Grading results (`st.session_state['grading_results']`)
- Cross-page navigation hints

## Testing

### Test Setup

Tests use Playwright for browser automation:

```bash
# Install test dependencies
pip install pytest pytest-playwright playwright
playwright install chromium

# Run tests
pytest tests/ -v -s
```

### Test Structure

```python
# tests/test_sidebar.py
class TestSidebarVisibility:
    def test_sidebar_expanded_by_default(self, page: Page):
        """Test that sidebar is visible on load."""

    def test_sidebar_has_navy_background(self, page: Page):
        """Test Navy Blue background color."""

    def test_expand_button_styling_when_collapsed(self, page: Page):
        """Test expand button has proper styling."""
```

### Running Tests

```bash
# Terminal 1: Start Streamlit
streamlit run app.py --server.port 8502 --server.headless true

# Terminal 2: Run tests
pytest tests/test_sidebar.py -v
```

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
4. Follow the Navy Blue header pattern for consistency

### Adding a New Database Table

1. Add `CREATE TABLE` in `init_db()` in `database.py`
2. Add CRUD functions following existing patterns
3. Delete `data/grader.db` to recreate schema (or use migrations)

### Adding New Settings

1. Use `get_setting(key, default)` and `set_setting(key, value)`
2. Settings are stored as strings; use JSON for complex values

### Adding New Tests

1. Create test file in `tests/` directory
2. Use `page: Page` fixture from pytest-playwright
3. Target elements using `[data-testid="..."]` selectors
4. Save screenshots to `tests/screenshots/`

## Conventions

### Code Style

- Use `st.session_state` for maintaining state between reruns
- All database operations go through `modules/database.py`
- Pages use Streamlit's native components (`st.dataframe`, `st.form`, etc.)
- Error handling: use `st.error()` and `st.success()` for user feedback
- Follow Navy Blue & White color scheme for custom HTML

### UI Patterns

- Use `st.form()` for data entry to prevent rerun on each input
- Use `st.expander()` for collapsible sections
- Use `st.columns()` for side-by-side layouts
- Use `st.data_editor()` for editable tables
- Page headers: Navy Blue background, white text, 8px border-radius

### Database Patterns

- Always use context manager: `with get_connection() as conn:`
- Return `dict(row)` for single records, `[dict(row) for row in rows]` for lists
- Use `ON CONFLICT ... DO UPDATE` for upserts

## Known Limitations

- Single-user application (no authentication)
- SQLite limits concurrent writes
- Large file uploads may be slow
- No undo functionality (use exports for backup)

## Troubleshooting

### Sidebar Not Visible
- Check browser console for CSS errors
- Hard refresh (Ctrl+Shift+R) to clear cache
- Verify `styles.apply_custom_css()` is called in `app.py`

### Database Errors
- Delete `data/grader.db` to recreate schema
- Check file permissions on `data/` directory

### Test Failures
- Ensure Streamlit is running on port 8502
- Wait for app to fully load (tests have 3s timeout)
- Check `tests/screenshots/` for visual debugging
