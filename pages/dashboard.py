import streamlit as st

from utils.auth import require_admin
from database.models import (
    get_total_users,
    get_all_users
)

require_admin()

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛠️"
)

st.title("🛠️ Admin Dashboard")

st.metric(
    "Registered Users",
    get_total_users()
)

st.divider()

st.subheader("👥 Manage Users")

users = get_all_users()

if users:

    table = []

    for user in users:

        table.append({
            "ID": user["id"],
            "Name": user["full_name"],
            "Email": user["email"],
            "Role": user["role"]
        })

    st.dataframe(
        table,
        use_container_width=True
    )

else:

    st.info("No users found.")