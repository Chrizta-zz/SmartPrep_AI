import streamlit as st
from utils.ui_theme import page_header

page_header(
    "SmartPrep AI",
    "Your AI-powered academic assistant",
    "🎓"
)

st.markdown("## Welcome!")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📅\n\nAI Study Planner")

with col2:
    st.info("📄\n\nAI Document Tutor")

with col3:
    st.info("🤖\n\nAI Quiz Generator")

st.divider()

c1, c2 = st.columns(2)

with c1:
    if st.button("🔐 Login", use_container_width=True):
        st.switch_page("pages/login.py")

with c2:
    if st.button("📝 Register", use_container_width=True):
        st.switch_page("pages/registration.py")