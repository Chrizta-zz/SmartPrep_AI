import streamlit as st


# -----------------------------
# SESSION MANAGEMENT
# -----------------------------
def create_session(username, role):

    st.session_state["logged_in"] = True
    st.session_state["username"] = username
    st.session_state["role"] = role


def logout():

    st.session_state.clear()


# -----------------------------
# LOGIN STATUS
# -----------------------------
def is_logged_in():

    return st.session_state.get("logged_in", False)


def require_login():

    if not is_logged_in():

        st.warning("🔒 Please login first.")
        st.stop()


# -----------------------------
# ROLES
# -----------------------------
def is_admin():

    return st.session_state.get("role") == "admin"


def is_user():

    return st.session_state.get("role") == "user"


def require_admin():

    require_login()

    if not is_admin():

        st.error("⛔ Admin access only.")
        st.stop()


def require_user():

    require_login()

    if not is_user():

        st.error("⛔ User access only.")
        st.stop()