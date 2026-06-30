import streamlit as st
from utils.auth import require_login

require_login()

st.title("📈 Progress Tracker")

st.write("View your learning progress and performance.")