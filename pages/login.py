import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.models import login_user

from utils.auth import create_session
from utils.ui_theme import page_header, card




page_header(
    "Welcome Back",
    "Sign in to continue your SmartPrep AI journey.",
    "🎓"
)

# Center the login form
left, center, right = st.columns([1, 2, 1])

with center:

    card("""
    <div style="text-align:center;">
        <h2>🔐 Login</h2>
        <p style="color:#9CA3AF;">
            Enter your credentials to access SmartPrep AI.
        </p>
    </div>
    """)

    email = st.text_input(
        "📧 Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "🔑 Password",
        type="password",
        placeholder="Enter your password"
    )

    if st.button("🚀 Login", use_container_width=True):

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
                    f"Welcome back, {user['name']} 👋"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption(
        "🎓 SmartPrep AI • Your AI-Powered Learning Assistant"
    )