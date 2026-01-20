# Grader - Technical Documentation

## Project Overview

A professional Streamlit-based grading application for educators to manage classes, students, assignments, and grades with comprehensive auto-grading capabilities.

**Repository:** https://github.com/bomino/grader

## Recent Changes (Version 1.0)

- **Tab-Based Navigation**: Replaced sidebar with intuitive tab navigation for better UX
- **Student ID Support**: Added unique student identifiers for academic institutions
- **Database Migrations**: Automatic schema updates for existing databases
- **Comprehensive Help**: Built-in documentation with quick start guide and workflows
- **WCAG Compliance**: Ensured white text on all colored backgrounds for accessibility
- **Professional Footer**: Added application footer with version information
- **Improved Statistics**: Dashboard now shows total grades count
- **Better Error Handling**: Clear guidance when prerequisites are missing

## Tech Stack

- **Python 3.8+** - Core language
- **Streamlit** - Web UI framework
- **SQLite** - Embedded database
- **Pandas** - Data manipulation and display
- **openpyxl** - Excel file generation
- **Playwright** - UI testing

## Project Structure

```
Grader/
├── app.py                    # Main entry point with tab navigation
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest configuration
├── README.md                # User documentation
├── CLAUDE.md                # Technical documentation (this file)
├── .gitignore               # Git ignore rules
│
├── data/
│   └── grader.db            # SQLite database (auto-created)
│
├── docs/
│   └── USER_GUIDE.md        # Comprehensive user guide
│
├── modules/
│   ├── __init__.py
│   ├── database.py          # All database operations & migrations
│   ├── styles_tabbed.py     # CSS theming for tab-based UI
│   └── pages/
│       ├── __init__.py
│       ├── classes.py       # Class management UI
│       ├── students.py      # Student roster with IDs
│       ├── assignments.py   # Assignment management UI
│       ├── grade_entry.py   # Manual grade entry UI
│       ├── auto_grade.py    # Answer keys & auto-grading UI
│       ├── gradebook.py     # Gradebook view & exports
│       ├── settings.py      # Grade scale configuration
│       └── help_guide.py    # In-app help documentation
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_sidebar.py      # Legacy tests (to be updated)
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

### Navigation System

The application uses a **tab-based navigation system** instead of sidebar navigation, providing a cleaner and more accessible interface.

### Color Palette

The application uses a professional Navy Blue & White theme defined in `modules/styles_tabbed.py`:

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

`modules/styles_tabbed.py` provides:
- `apply_custom_css()` - Applies global CSS styles for tab navigation
- `get_stat_card_style(variant)` - Colored stat card styling

### CSS Features

- Tab-based navigation with clear visual hierarchy
- WCAG-compliant white text on all colored backgrounds
- Consistent Navy Blue page headers
- Professional card and stat components
- Styled form inputs and buttons
- Responsive design optimized for desktop use

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
    student_id TEXT,  -- Unique identifier (e.g., university ID)
    class_id INTEGER NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
);
CREATE INDEX idx_student_id ON students(student_id);

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
migrate_database()   # Apply migrations to existing databases

# CRUD Operations (per entity)
get_all_*()          # List all records
get_*_by_id(id)      # Get single record
add_*(...)           # Create new record
update_*(id, ...)    # Update existing record
delete_*(id)         # Delete record

# Special operations
bulk_add_students()  # Bulk insert from CSV with student IDs
bulk_set_grades()    # Upsert multiple grades
get_grade_scale()    # Get JSON settings
set_grade_scale()    # Save JSON settings
get_total_counts()   # Dashboard statistics (returns dict)
```

### Database Migrations

The application supports automatic database migrations to update existing databases with new features:

```python
def migrate_database(conn):
    """Apply migrations to existing databases."""
    cursor = conn.cursor()

    # Check if student_id column exists
    cursor.execute("PRAGMA table_info(students)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'student_id' not in columns:
        # Add student_id column to existing databases
        cursor.execute("ALTER TABLE students ADD COLUMN student_id TEXT")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_id ON students(student_id)")
        conn.commit()
```

Migrations run automatically during `init_db()` to ensure backward compatibility.

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

### Adding a New Tab

1. Create `modules/pages/newpage.py` with a `render()` function
2. Import in `app.py`: `from modules.pages import newpage`
3. Add a new tab to the `st.tabs()` list in `app.py`
4. Add a new `with tabs[n]:` block calling `newpage.render()`
5. Follow the Navy Blue header pattern for consistency

### Adding a New Database Table

1. Add `CREATE TABLE` in `init_db()` in `database.py`
2. Add CRUD functions following existing patterns
3. For existing databases, add a migration in `migrate_database()`
4. Delete `data/grader.db` to recreate schema (or migrations will handle it)

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

## Key Features

### Student ID Support

Students can have unique identifiers (e.g., university ID numbers) in addition to names:
- Optional but recommended for larger classes
- Used for matching in auto-grading
- Helps prevent duplicate entries
- Indexed for fast lookups

### Auto-Grading with Student ID Matching

The auto-grade system can match students by either:
- Student name (exact match)
- Student ID (if provided)
- Flexible CSV/Excel format support

### Comprehensive Help System

The application includes an in-app help guide (`modules/pages/help_guide.py`) with:
- Quick Start guide for new users
- Feature explanations with examples
- Common workflows and best practices
- FAQ section
- Tips & Tricks for efficient use

### Export Capabilities

Multiple export formats for gradebook data:
- **Excel (.xlsx)**: Formatted spreadsheet with statistics
- **CSV (.csv)**: Raw data for further analysis
- **Text Summary (.txt)**: Human-readable report

## Known Limitations

- Single-user application (no authentication)
- SQLite limits concurrent writes
- Large file uploads may be slow
- No undo functionality (use exports for backup)

## Troubleshooting

### Navigation Issues
- Tab navigation requires Streamlit 1.32.0 or higher
- Hard refresh (Ctrl+Shift+R) to clear cache
- Verify `styles_tabbed.apply_custom_css()` is called in `app.py`

### Database Errors
- Migrations handle schema updates automatically
- Delete `data/grader.db` to recreate schema from scratch
- Check file permissions on `data/` directory

### Auto-Grade File Uploader Not Visible
- Ensure you've created a class first
- Create at least one assignment for the class
- Create an answer key before uploading responses
- Add at least one student to the class

### Test Failures
- Ensure Streamlit is running on port 8502
- Wait for app to fully load (tests have 3s timeout)
- Check `tests/screenshots/` for visual debugging
- Note: Some tests may need updating for tab navigation
