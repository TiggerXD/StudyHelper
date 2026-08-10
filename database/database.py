import sqlite3
from pathlib import Path

# Database location
BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "users.db"


# Connect to database
def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# Initialize database
def initialize_database():
    conn = connect()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Assignments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            created_by TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Add a new user
def add_user(student_id, name, role="student"):
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (student_id, name, role)
            VALUES (?, ?, ?)
            """,
            (student_id, name, role)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# Login user
def login(student_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE student_id = ?
        """,
        (student_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# Create an assignment
def create_assignment(title, subject, description, due_date, created_by):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO assignments
        (title, subject, description, due_date, created_by)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, subject, description, due_date, created_by)
    )

    conn.commit()

    assignment_id = cursor.lastrowid

    conn.close()

    return assignment_id


# Get all assignments
def get_assignments():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM assignments
        ORDER BY due_date ASC
        """
    )

    assignments = cursor.fetchall()

    conn.close()

    return assignments


# Get one assignment
def get_assignment(assignment_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM assignments
        WHERE id = ?
        """,
        (assignment_id,)
    )

    assignment = cursor.fetchone()

    conn.close()

    return assignment