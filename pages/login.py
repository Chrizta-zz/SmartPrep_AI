import streamlit as st
from database.models import login_user
from utils.ui_theme import page_header

page_header("Login", "Welcome back! Sign in to continue.", "🔐")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    user = login_user(email, password)

    if user:
        st.success(f"Welcome {user['full_name']}!")

        st.session_state["logged_in"] = True
        st.session_state["user"] = dict(user)

    else:
        st.error("Invalid Email or Password")