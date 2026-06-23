import mysql.connector
import streamlit as st


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            port=int(st.secrets["DB_PORT"]),
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            database=st.secrets["DB_NAME"]
        )
        return conn
    except Exception as e:
        st.error(f"Error de conexión a la base de datos: {e}")
        return None