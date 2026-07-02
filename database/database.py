import sqlite3
import bcrypt

DATABASE_NAME = "database/smartprep.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# USERS TABLE
# -----------------------------
def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# STUDY PLAN TABLE
# -----------------------------
def create_study_plan_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_plans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        subject TEXT,
        confidence TEXT,
        exam_date TEXT,
        study_hours INTEGER,
        study_plan TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# DEFAULT ADMIN
# -----------------------------
def create_default_admin():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        ("admin@smartprep.com",)
    )

    admin = cursor.fetchone()

    if admin is None:

        hashed_password = bcrypt.hashpw(
            "admin123".encode(),
            bcrypt.gensalt()
        ).decode()

        cursor.execute("""
        INSERT INTO users(
            full_name,
            email,
            password,
            role
        )
        VALUES(?,?,?,?)
        """, (
            "Administrator",
            "admin@smartprep.com",
            hashed_password,
            "admin"
        ))

        conn.commit()

    conn.close()


# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
create_tables()
create_study_plan_table()
create_default_admin()