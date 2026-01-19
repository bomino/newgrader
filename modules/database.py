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
        return {"classes": class_count, "students": student_count}

# Initialize database on module import
init_db()
