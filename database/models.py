import bcrypt
from database.database import get_connection


def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def register_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(password)

    try:
        cursor.execute("""
        INSERT INTO users(full_name,email,password)
        VALUES(?,?,?)
        """, (name, email, hashed))

        conn.commit()
        return True

    except:

        return False

    finally:

        conn.close()


def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        if bcrypt.checkpw(
            password.encode(),
            user["password"].encode()
        ):
            return user

    return None