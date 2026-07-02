import streamlit as st

from utils.auth import is_logged_in, is_admin
from utils.ui_theme import apply_theme

st.set_page_config(
    page_title="SmartPrep AI",
    page_icon="🎓",
    layout="wide"
)

apply_theme()

# -----------------------------
# GUEST
# -----------------------------
if not is_logged_in():

    pages = [
        st.Page(
            "pages/login.py",
            title="Login",
            icon="🔐",
            default=True
        ),
        st.Page(
            "pages/registration.py",
            title="Registration",
            icon="📝"
        )
    ]

# -----------------------------
# ADMIN
# -----------------------------
elif is_admin():

    st.sidebar.success(f"👋 {st.session_state['username']}")
    st.sidebar.write("**Role:** Administrator")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

    pages = [
        st.Page(
            "pages/admin.py",
            title="Dashboard",
            icon="🛠️",
            default=True
        )
    ]

# -----------------------------
# USER
# -----------------------------
else:

    st.sidebar.success(f"👋 {st.session_state['username']}")
    st.sidebar.write("**Role:** User")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

    pages = [
        st.Page(
            "pages/planner.py",
            title="AI Study Planner",
            icon="📅",
            default=True
        ),
        st.Page(
            "pages/document_chat.py",
            title="AI Document Tutor",
            icon="📄"
        ),
        st.Page(
            "pages/quiz.py",
            title="AI Quiz Generator",
            icon="🤖"
        )
    ]

pg = st.navigation(pages)
pg.run()