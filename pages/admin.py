import streamlit as st
import pandas as pd
from database.database import get_connection

st.title("🗄 Database Viewer")

conn = get_connection()

df = pd.read_sql_query(
    "SELECT id, full_name, email FROM users",
    conn
)

conn.close()

st.subheader("Registered Users")

st.dataframe(df, use_container_width=True)