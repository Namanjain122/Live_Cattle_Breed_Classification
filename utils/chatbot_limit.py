from utils.db import get_connection

# =========================================
# CHECK CHATBOT LIMIT
# =========================================
def can_use_chatbot(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT query_count
        FROM chatbot_usage
        WHERE user_id=%s
        """,
        (user_id,)
    )

    count = cursor.fetchone()[0]

    return count < 1


# =========================================
# UPDATE QUERY COUNT
# =========================================
def increase_query_count(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE chatbot_usage
        SET query_count = query_count + 1
        WHERE user_id=%s
        """,
        (user_id,)
    )

    conn.commit()