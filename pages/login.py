import streamlit as st

from database.models import login_user
from utils.auth import create_session
from utils.ui_theme import page_header

page_header(
    "Login",
    "Welcome back! Sign in to SmartPrep AI.",
    "🔐"
)

email = st.text_input(
    "Email"
)

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login", use_container_width=True):

    if not email or not password:
        st.warning("Please enter both email and password.")

    else:

        user = login_user(email, password)

        if user:

            create_session(
                user["name"],
                user["role"]
            )

            st.session_state["user"] = user

            st.success(
                f"Welcome, {user['name']}!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid email or password."
            )