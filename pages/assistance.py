import streamlit as st

from utils.auth import require_login

require_login()

st.title("📚 Learning Assistant")

st.write("Upload notes and ask questions about your study material.")