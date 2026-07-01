import streamlit as st
import pandas as pd
from database.database import get_connection
from utils.ui_theme import page_header, section_title

page_header("Database Viewer", "All registered SmartPrep AI users.", "🗄")

conn = get_connection()

df = pd.read_sql_query(
    "SELECT id, full_name, email FROM users",
    conn
)

conn.close()

section_title("Registered Users", "👥")

st.dataframe(df, use_container_width=True)