import streamlit as st

from utils.auth import is_logged_in, is_admin
from utils.ui_theme import apply_theme

st.set_page_config(
    page_title="SmartPrep AI",
    page_icon="🎓",
    layout="wide"
)

apply_theme()

# ----------------------------
# BEFORE LOGIN
# ----------------------------
if not is_logged_in():

    pages = [

        st.Page(
            "pages/home.py",
            title="Home",
            icon="🏠",
            default=True
        ),

        st.Page(
            "pages/login.py",
            title="Login",
            icon="🔐"
        ),

        st.Page(
            "pages/registration.py",
            title="Register",
            icon="📝"
        ),
    ]

# ----------------------------
# ADMIN
# ----------------------------
elif is_admin():

    pages = [

        st.Page(
            "pages/admin.py",
            title="Dashboard",
            icon="🛠",
            default=True
        ),

    ]

# ----------------------------
# USER
# ----------------------------
else:

    pages = [

        st.Page(
            "pages/dashboard.py",
            title="Dashboard",
            icon="🏠",
            default=True
        ),

        st.Page(
            "pages/planner.py",
            title="Study Planner",
            icon="📅"
        ),

        st.Page(
            "pages/document_chat.py",
            title="Document Tutor",
            icon="📄"
        ),

        st.Page(
            "pages/quiz.py",
            title="Quiz Generator",
            icon="🤖"
        ),

    ]

    with st.sidebar:

        st.success(f"👋 {st.session_state['username']}")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

pg = st.navigation(pages)
pg.run()