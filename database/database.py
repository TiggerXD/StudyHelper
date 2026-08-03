import sqlite3

DB_NAME = "database/users.db"


def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def initialize_database():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (student_id TEXT PRIMARY KEY, name TEXT, role TEXT)")

    conn.commit()
    conn.close()

def add_user(student_id, name, role="student"):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", (student_id, name, role))

    conn.commit()
    conn.close()

def login(student_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE student_id=?",
        (student_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user