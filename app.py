import streamlit as st
from utils.ui_theme import apply_theme, page_header, section_title, divider

if st.session_state.get("logged_in"):

    user = st.session_state["user"]

    st.sidebar.success(f"👋 {user['full_name']}")

    if st.sidebar.button("🚪 Logout"):

        st.session_state.clear()

        st.rerun()

st.set_page_config(
    page_title="SmartPrep AI",
    page_icon="🎓",
    layout="wide"
)

page_header("SmartPrep AI", "Multi-Agent Exam Preparation Assistant", "🎓")

divider()

section_title("Dashboard", "📊")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Subjects", "5")
col2.metric("Study Hours", "24")
col3.metric("Quiz Score", "82%")
col4.metric("Progress", "65%")

divider()

section_title("Today's Study Plan", "📅")

st.success("✔ Python - 2 Hours")
st.info("✔ Artificial Intelligence - 1.5 Hours")
st.warning("✔ Cloud Computing - 1 Hour")

divider()

section_title("Quick Actions", "🔥")

c1, c2, c3 = st.columns(3)

with c1:
    st.button("📅 Generate Study Plan")

with c2:
    st.button("📄 Upload Notes")

with c3:
    st.button("📝 Take Quiz")