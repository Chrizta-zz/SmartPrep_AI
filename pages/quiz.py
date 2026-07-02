import streamlit as st
from utils.auth import require_login
from utils.ui_theme import page_header

from agents.quiz_agent import generate_quiz, generate_quiz_from_context
from utils.quiz_parser import evaluate_quiz
# from utils.vector_store import search_similar_chunks
from utils.document_loader import load_pdf_text
from utils.auth import require_user

require_user()

page_header("Quiz Generator", "Generate quizzes from your uploaded notes.", "📝")





# =========================
# MODE SWITCH
# =========================
mode = st.radio("Choose Quiz Mode", ["Topic Quiz", "PDF Quiz"])

# =========================
# SESSION INIT
# =========================
if "quiz" not in st.session_state:
    st.session_state.quiz = None
    st.session_state.answers = {}

# ==========================================================
# 🟢 1. TOPIC QUIZ MODE
# ==========================================================
elif mode == "PDF Quiz":

    st.subheader("📄 PDF-Based Quiz (RAG)")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    col1, col2 = st.columns(2)

    with col1:
        num_questions = st.number_input("Number of Questions", 1, 20, 5, key="pdf_q")

    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="pdf_d")

    qtype = st.selectbox("Question Type", ["MCQ", "True/False", "Short Answer"], key="pdf_t")

    if st.button("🚀 Generate Quiz from PDF"):

        if uploaded_file is None:
            st.warning("Please upload a PDF")
            st.stop()

        with st.spinner("Reading PDF..."):
            text = load_pdf_text(uploaded_file)

        # ✅ REAL CHUNKING
        chunks = text.split(". ")
        chunks = [c.strip() for c in chunks if len(c.strip()) > 40]

        # ✅ BUILD FAISS INDEX
        from utils.vector_store import build_index, search_similar_chunks

        build_index(chunks)

        # ✅ SEMANTIC SEARCH
        context_chunks = search_similar_chunks(
            query="important concepts for quiz",
            k=5
        )

        context = "\n".join(context_chunks)

        with st.spinner("Generating quiz from RAG context..."):
            quiz_data = generate_quiz_from_context(
                context,
                num_questions,
                difficulty,
                qtype
            )

        if not quiz_data or "questions" not in quiz_data:
            st.error("Failed to generate quiz")
            st.stop()

        st.session_state.quiz = quiz_data["questions"]
        st.session_state.answers = {}
        st.success("Quiz generated using REAL RAG!")
# ==========================================================
# 🔵 2. PDF (RAG) QUIZ MODE - FIXED
# ==========================================================
elif mode == "PDF Quiz":

    st.subheader("📄 PDF-Based Quiz (RAG)")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    col1, col2 = st.columns(2)

    with col1:
        num_questions = st.number_input("Number of Questions", 1, 20, 5, key="pdf_q")

    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="pdf_d")

    qtype = st.selectbox("Question Type", ["MCQ", "True/False", "Short Answer"], key="pdf_t")

    if st.button("🚀 Generate Quiz from PDF"):

        if uploaded_file is None:
            st.warning("Please upload a PDF")
            st.stop()

        with st.spinner("Reading PDF..."):
            text = load_pdf_text(uploaded_file)

        # ✅ FIX: safe chunking fallback (no FAISS dependency needed)
        chunks = text.split("\n")
        chunks = [c.strip() for c in chunks if len(c.strip()) > 30]

        # take top chunks
        context = "\n".join(chunks[:8])

        with st.spinner("Generating quiz from document..."):
            quiz_data = generate_quiz_from_context(
                context,
                num_questions,
                difficulty,
                qtype
            )

        if not quiz_data or "questions" not in quiz_data:
            st.error("Failed to generate quiz from PDF")
            st.stop()

        st.session_state.quiz = quiz_data["questions"]
        st.session_state.answers = {}
        st.success("Quiz generated from PDF!")

# ==========================================================
# 📋 DISPLAY QUIZ (COMMON FOR BOTH MODES)
# ==========================================================
if st.session_state.quiz:

    st.divider()
    st.subheader("📋 Your Quiz")

    for i, q in enumerate(st.session_state.quiz):

        st.markdown(f"### Q{i+1}. {q['question']}")

        options = q.get("options", [])

        if options:
            answer = st.radio(
                f"Select answer Q{i+1}",
                options,
                key=f"q_{i}"
            )
        else:
            answer = st.text_input(
                f"Your answer Q{i+1}",
                key=f"q_{i}"
            )

        st.session_state.answers[i] = answer

        st.write("---")

# ==========================================================
# 📊 SUBMIT QUIZ
# ==========================================================
if st.session_state.quiz:

    if st.button("📊 Submit Quiz"):

        correct, total, accuracy, results = evaluate_quiz(
            st.session_state.quiz,
            st.session_state.answers
        )

        st.success(f"Score: {correct}/{total}")
        st.info(f"Accuracy: {accuracy:.2f}%")

        st.divider()
        st.subheader("📌 Review Answers")

        for r in results:

            if r["is_correct"]:
                st.success(f"✔ {r['question']}")
            else:
                st.error(f"❌ {r['question']}")

            st.write(f"**Correct Answer:** {r['correct_answer']}")
            st.write(f"**Your Answer:** {r['user_answer']}")
            st.write(f"**Explanation:** {r['explanation']}")
            st.write("---")