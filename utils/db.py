from dotenv import load_dotenv
import mysql.connector
import streamlit as st
import os

# Load environment variables
load_dotenv()


def get_connection():
    host = os.getenv("DB_HOST") or st.secrets["DB_HOST"]
    user = os.getenv("DB_USER") or st.secrets["DB_USER"]
    password = os.getenv("DB_PASSWORD") or st.secrets["DB_PASSWORD"]
    database = os.getenv("DB_NAME") or st.secrets["DB_NAME"]
    port = os.getenv("DB_PORT") or st.secrets["DB_PORT"]

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=int(port)
    )
