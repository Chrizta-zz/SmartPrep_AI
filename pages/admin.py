import streamlit as st


from utils.auth import require_admin

require_admin()

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛠️",
    layout="wide"
)

# -------------------------------
# HEADER
# -------------------------------
st.title("🛠️ SmartPrep AI Admin Dashboard")
st.write("Welcome, **Administrator** 👋")

st.divider()

# -------------------------------
# DASHBOARD METRICS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Users", "0")

with col2:
    st.metric("📅 Study Plans", "0")

with col3:
    st.metric("📄 Documents", "0")

with col4:
    st.metric("🤖 Quizzes", "0")

st.divider()

# -------------------------------
# MANAGE USERS
# -------------------------------
st.subheader("👥 Manage Users")

st.info("User management will appear here.")

st.divider()

# -------------------------------
# ANALYTICS
# -------------------------------
st.subheader("📈 Analytics")

st.info("Analytics charts will appear here.")

st.divider()

# -------------------------------
# RECENT ACTIVITY
# -------------------------------
st.subheader("📝 Recent Activity")

st.info("Recent activities will appear here.")