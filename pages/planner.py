import streamlit as st

from utils.auth import require_login

require_login()

st.title("📅 Study Planner")

st.write("This module will generate a personalized study schedule.")