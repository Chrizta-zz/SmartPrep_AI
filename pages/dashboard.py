import streamlit as st

from utils.auth import require_user
from utils.ui_theme import (
    page_header,
    dashboard_card,
    feature_card,
    info_card,
)

require_user()

# from utils.navbar import top_navbar

menu = None

if menu == "🏠 Dashboard":
    st.switch_page("pages/dashboard.py")

elif menu == "📅 Study Planner":
    st.switch_page("pages/planner.py")

elif menu == "📄 Document Tutor":
    st.switch_page("pages/document_chat.py")

elif menu == "🤖 Quiz Generator":
    st.switch_page("pages/quiz.py")

elif menu == "🚪 Logout":
    st.session_state.clear()
    st.switch_page("pages/login.py")

page_header(
    "SmartPrep AI",
    "Your Personal AI Study Assistant",
    "🎓"
)

st.write("")

st.subheader("🚀 AI Modules")

c1,c2,c3 = st.columns(3)

with c1:
    dashboard_card("Study Planner","AI","📅")

with c2:
    dashboard_card("Document Tutor","RAG","📄")

with c3:
    dashboard_card("Quiz Generator","LLM","🤖")


st.divider()


st.subheader("📈 Statistics")

a,b,c,d = st.columns(4)

with a:
    st.metric("Study Plans","12","+2")

with b:
    st.metric("Quizzes","28","+6")

with c:
    st.metric("Documents","5","+1")

with d:
    st.metric("Learning Streak","8 Days","+1")


st.divider()


st.subheader("✨ Features")

x,y,z = st.columns(3)

with x:

    feature_card(
        "📅",
        "AI Planner",
        "Generate personalized study schedules."
    )

with y:

    feature_card(
        "📄",
        "Document Tutor",
        "Upload notes and chat with your PDFs."
    )

with z:

    feature_card(
        "🤖",
        "Quiz Generator",
        "Generate quizzes from any topic or document."
    )


st.divider()

info_card(
    "💡 AI Tip",
    "Study consistently. Small daily progress leads to big improvements over time."
)

st.divider()

st.subheader("⚡ Quick Actions")

q1,q2,q3 = st.columns(3)

with q1:
    if st.button("📅 Create Study Plan", use_container_width=True):
        st.switch_page("pages/planner.py")

with q2:
    if st.button("📄 Upload Document", use_container_width=True):
        st.switch_page("pages/document_chat.py")

with q3:
    if st.button("🤖 Generate Quiz", use_container_width=True):
        st.switch_page("pages/quiz.py")