import streamlit as st
from utils.auth import require_login

require_login()

st.title("📝 Quiz Generator")

st.write("Generate quizzes from your uploaded notes.")