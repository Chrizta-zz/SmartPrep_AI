import streamlit as st

from agents.document_agent import (
    process_document,
    ask_document
)
from utils.auth import require_user
from utils.ui_theme import page_header

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

st.set_page_config(
    page_title="AI Document Tutor",
    page_icon="📄"
)

page_header(
    "AI Document Tutor",
    "Upload your notes and ask questions using AI + RAG.",
    "📄"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload PDF, DOCX or TXT",
    type=["pdf", "docx", "txt"]
)

if uploaded_file is not None:

    # Only process once
    if (
        st.session_state.document_name
        != uploaded_file.name
    ):

        with st.spinner("Processing document..."):

            st.session_state.vectorstore = process_document(
                uploaded_file
            )

            st.session_state.document_name = uploaded_file.name
            st.session_state.messages = []

        st.success("✅ Document processed successfully!")

# -----------------------------
# CHAT
# -----------------------------
if st.session_state.vectorstore is not None:

    st.subheader("💬 Ask Questions")

    # Show previous chat
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User question
    question = st.chat_input(
        "Ask anything from your document..."
    )

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = ask_document(
                    st.session_state.vectorstore,
                    question
                )

                st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

# -----------------------------
# RESET
# -----------------------------
if st.session_state.vectorstore is not None:

    if st.button("🔄 Reset Document"):

        st.session_state.vectorstore = None
        st.session_state.document_name = None
        st.session_state.messages = []

        st.rerun()