import streamlit as st
from database.models import register_user
from utils.ui_theme import page_header

page_header("Register", "Create your SmartPrep AI account to get started.", "📝")

name = st.text_input("Full Name")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Register"):

    success = register_user(
        name,
        email,
        password
    )

    if success:
        st.success("Registration Successful!")

    else:
        st.error("Email already exists.")