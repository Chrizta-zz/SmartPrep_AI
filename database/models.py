import bcrypt

from database.database import get_connection


# -----------------------------
# PASSWORD HASHING
# -----------------------------
def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


# -----------------------------
# REGISTER USER
# -----------------------------
def register_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:

        cursor.execute("""
        INSERT INTO users(
            full_name,
            email,
            password,
            role
        )
        VALUES(?,?,?,?)
        """, (
            name,
            email,
            hashed_password,
            "user"
        ))

        conn.commit()

        return True

    except Exception as e:

        print(e)
        return False

    finally:

        conn.close()


# -----------------------------
# LOGIN USER
# -----------------------------
def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return None

    if bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    ):

        return {
            "id": user["id"],
            "name": user["full_name"],
            "email": user["email"],
            "role": user["role"]
        }

    return None


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
def get_total_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE role='user'"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        full_name,
        email,
        role
    FROM users
    ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()

    return users