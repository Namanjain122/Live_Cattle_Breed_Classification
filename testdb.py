import mysql.connector

try:

    conn = mysql.connector.connect(
        host="localhost",
        user="cattle_user",
        password="naman@1q2w",  # change if needed
        database="cattle_app"
    )

    print("✅ Connected Successfully")

except Exception as e:

    print("❌ Error:", e)
