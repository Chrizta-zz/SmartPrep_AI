import streamlit as st

from utils.auth import require_login
from utils.ui_theme import page_header
from utils.document_loader import load_document
from agents.document_agent import create_vectorstore, ask_document

require_login()

st.set_page_config(
    page_title="AI Document Tutor",
    page_icon="📄"
)

page_header(
    "AI Document Tutor",
    "Upload your notes and ask questions.",
    "📄"
)

uploaded_file = st.file_uploader(
    "Upload PDF, DOCX or TXT",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:

    # Read and create vector store only once
    if "document_text" not in st.session_state:

        with st.spinner("Reading and indexing document..."):
            document_text = load_document(uploaded_file)
            create_vectorstore(document_text)

            st.session_state["document_text"] = document_text

        st.success("Document uploaded successfully!")

    st.subheader("Document Preview")

    st.text_area(
        "",
        st.session_state["document_text"][:3000],
        height=300
    )

    question = st.chat_input("Ask anything about your document...")

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Thinking..."):
            answer = ask_document(question)

        with st.chat_message("assistant"):
            st.write(answer)