import sqlite3
import os
from pathlib import Path
from contextlib import contextmanager

# Database path
DB_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DB_DIR / "grader.db"

def ensure_db_dir():
    """Ensure the data directory exists."""
    DB_DIR.mkdir(parents=True, exist_ok=True)

@contextmanager
def get_connection():
    """Context manager for database connections."""
    ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    """Initialize database with required tables."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Classes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class_id INTEGER NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
            )
        """)

        # Assignments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class_id INTEGER NOT NULL,
                max_points REAL NOT NULL DEFAULT 100,
                weight REAL NOT NULL DEFAULT 1.0,
                due_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
            )
        """)

        # Grades table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grades (
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
            )
        """)

        # Answer keys table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS answer_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id INTEGER NOT NULL,
                question_num INTEGER NOT NULL,
                correct_answer TEXT NOT NULL,
                points REAL NOT NULL DEFAULT 1.0,
                question_type TEXT DEFAULT 'multiple_choice',
                FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE,
                UNIQUE(assignment_id, question_num)
            )
        """)

        # Settings table for grade scale
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

# ==================== CLASS OPERATIONS ====================

def get_all_classes():
    """Get all classes."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]

def get_class_by_id(class_id):
    """Get a class by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes WHERE id = ?", (class_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def add_class(name):
    """Add a new class."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classes (name) VALUES (?)", (name,))
        return cursor.lastrowid

def update_class(class_id, name):
    """Update a class name."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE classes SET name = ? WHERE id = ?", (name, class_id))
        return cursor.rowcount > 0

def delete_class(class_id):
    """Delete a class and all associated students."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        return cursor.rowcount > 0

# ==================== STUDENT OPERATIONS ====================

def get_students_by_class(class_id):
    """Get all students in a class."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE class_id = ? ORDER BY name",
            (class_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

def get_all_students():
    """Get all students with their class names."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, c.name as class_name
            FROM students s
            JOIN classes c ON s.class_id = c.id
            ORDER BY c.name, s.name
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_student_by_id(student_id):
    """Get a student by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def add_student(name, class_id, email=None):
    """Add a new student."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, class_id, email) VALUES (?, ?, ?)",
            (name, class_id, email)
        )
        return cursor.lastrowid

def update_student(student_id, name, class_id=None, email=None):
    """Update a student."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if class_id is not None:
            cursor.execute(
                "UPDATE students SET name = ?, class_id = ?, email = ? WHERE id = ?",
                (name, class_id, email, student_id)
            )
        else:
            cursor.execute(
                "UPDATE students SET name = ?, email = ? WHERE id = ?",
                (name, email, student_id)
            )
        return cursor.rowcount > 0

def delete_student(student_id):
    """Delete a student."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        return cursor.rowcount > 0

def bulk_add_students(students, class_id):
    """Bulk add students to a class. students is a list of dicts with 'name' and optional 'email'."""
    with get_connection() as conn:
        cursor = conn.cursor()
        added = 0
        for student in students:
            try:
                cursor.execute(
                    "INSERT INTO students (name, class_id, email) VALUES (?, ?, ?)",
                    (student.get('name'), class_id, student.get('email'))
                )
                added += 1
            except sqlite3.IntegrityError:
                continue
        return added

def get_student_count_by_class(class_id):
    """Get the number of students in a class."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE class_id = ?", (class_id,))
        return cursor.fetchone()[0]

def get_total_counts():
    """Get total counts for dashboard."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM classes")
        class_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM assignments")
        assignment_count = cursor.fetchone()[0]
        return {"classes": class_count, "students": student_count, "assignments": assignment_count}

# ==================== ASSIGNMENT OPERATIONS ====================

def get_assignments_by_class(class_id):
    """Get all assignments for a class."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM assignments WHERE class_id = ? ORDER BY due_date, name",
            (class_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

def get_all_assignments():
    """Get all assignments with class names."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, c.name as class_name
            FROM assignments a
            JOIN classes c ON a.class_id = c.id
            ORDER BY c.name, a.due_date, a.name
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_assignment_by_id(assignment_id):
    """Get an assignment by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assignments WHERE id = ?", (assignment_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def add_assignment(name, class_id, max_points=100, weight=1.0, due_date=None):
    """Add a new assignment."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO assignments (name, class_id, max_points, weight, due_date) VALUES (?, ?, ?, ?, ?)",
            (name, class_id, max_points, weight, due_date)
        )
        return cursor.lastrowid

def update_assignment(assignment_id, name, max_points=None, weight=None, due_date=None):
    """Update an assignment."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE assignments SET name = ?, max_points = ?, weight = ?, due_date = ? WHERE id = ?",
            (name, max_points, weight, due_date, assignment_id)
        )
        return cursor.rowcount > 0

def delete_assignment(assignment_id):
    """Delete an assignment."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
        return cursor.rowcount > 0

# ==================== GRADE OPERATIONS ====================

def get_grade(student_id, assignment_id):
    """Get a specific grade."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM grades WHERE student_id = ? AND assignment_id = ?",
            (student_id, assignment_id)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

def get_grades_by_assignment(assignment_id):
    """Get all grades for an assignment."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.*, s.name as student_name
            FROM grades g
            JOIN students s ON g.student_id = s.id
            WHERE g.assignment_id = ?
            ORDER BY s.name
        """, (assignment_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_grades_by_student(student_id):
    """Get all grades for a student."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.*, a.name as assignment_name, a.max_points, a.weight
            FROM grades g
            JOIN assignments a ON g.assignment_id = a.id
            WHERE g.student_id = ?
            ORDER BY a.due_date, a.name
        """, (student_id,))
        return [dict(row) for row in cursor.fetchall()]

def set_grade(student_id, assignment_id, points, comments=None):
    """Set or update a grade."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO grades (student_id, assignment_id, points, comments)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(student_id, assignment_id)
            DO UPDATE SET points = ?, comments = ?, updated_at = CURRENT_TIMESTAMP
        """, (student_id, assignment_id, points, comments, points, comments))
        return cursor.lastrowid

def bulk_set_grades(grades):
    """Bulk set grades. grades is a list of dicts with student_id, assignment_id, points, comments."""
    with get_connection() as conn:
        cursor = conn.cursor()
        for grade in grades:
            cursor.execute("""
                INSERT INTO grades (student_id, assignment_id, points, comments)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(student_id, assignment_id)
                DO UPDATE SET points = ?, comments = ?, updated_at = CURRENT_TIMESTAMP
            """, (
                grade['student_id'], grade['assignment_id'], grade['points'], grade.get('comments'),
                grade['points'], grade.get('comments')
            ))
        return len(grades)

# ==================== ANSWER KEY OPERATIONS ====================

def get_answer_key(assignment_id):
    """Get answer key for an assignment."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM answer_keys WHERE assignment_id = ? ORDER BY question_num",
            (assignment_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

def set_answer_key(assignment_id, questions):
    """Set answer key for an assignment. questions is a list of dicts with question_num, correct_answer, points, question_type."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Delete existing answer key
        cursor.execute("DELETE FROM answer_keys WHERE assignment_id = ?", (assignment_id,))
        # Insert new answers
        for q in questions:
            cursor.execute("""
                INSERT INTO answer_keys (assignment_id, question_num, correct_answer, points, question_type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                assignment_id,
                q['question_num'],
                q['correct_answer'],
                q.get('points', 1.0),
                q.get('question_type', 'multiple_choice')
            ))
        return len(questions)

def delete_answer_key(assignment_id):
    """Delete answer key for an assignment."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM answer_keys WHERE assignment_id = ?", (assignment_id,))
        return cursor.rowcount

# ==================== SETTINGS OPERATIONS ====================

def get_setting(key, default=None):
    """Get a setting value."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else default

def set_setting(key, value):
    """Set a setting value."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = ?
        """, (key, value, value))
        return True

def get_grade_scale():
    """Get the grade scale settings."""
    import json
    default_scale = {"A": 90, "B": 80, "C": 70, "D": 60, "F": 0}
    scale_json = get_setting("grade_scale", json.dumps(default_scale))
    return json.loads(scale_json)

def set_grade_scale(scale):
    """Set the grade scale."""
    import json
    return set_setting("grade_scale", json.dumps(scale))

# Initialize database on module import
init_db()
