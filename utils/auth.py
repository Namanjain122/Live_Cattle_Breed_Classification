import bcrypt

from utils.db import get_connection

# =========================================
# REGISTER USER
# =========================================
def register_user(username, phone, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    try:

        cursor.execute(
            """
            INSERT INTO users(
                username,
                phone,
                password
            )
            VALUES(%s, %s, %s)
            """,
            (
                username,
                phone,
                hashed_password
            )
        )

        conn.commit()

        # =========================================
        # GET USER ID
        # =========================================
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username=%s
            """,
            (username,)
        )

        user_id = cursor.fetchone()[0]

        # =========================================
        # INSERT CHATBOT LIMIT
        # =========================================
        cursor.execute(
            """
            INSERT INTO chatbot_usage(
                user_id,
                query_count
            )
            VALUES(%s, 0)
            """,
            (user_id,)
        )

        conn.commit()

        return True

    except Exception as e:

        print(e)

        return False

# =========================================
# LOGIN USER
# =========================================
def login_user(phone, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, password
        FROM users
        WHERE phone=%s
        """,
        (phone,)
    )

    user = cursor.fetchone()

    if user:

        user_id, username, hashed_password = user

        if bcrypt.checkpw(
            password.encode(),
            hashed_password.encode()
        ):

            return {
                "id": user_id,
                "username": username
            }

    return None