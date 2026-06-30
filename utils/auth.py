import streamlit as st

def is_logged_in():
    return st.session_state.get("logged_in", False)


def require_login():
    if not is_logged_in():
        st.warning("🔒 Please login to continue.")
        st.stop()