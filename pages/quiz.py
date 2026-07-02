import streamlit as st

from utils.auth import require_user
from utils.ui_theme import page_header
from utils.document_loader import load_pdf_text

from agents.quiz_agent import (
    generate_quiz,
    generate_quiz_from_context
)

from utils.quiz_parser import evaluate_quiz


# ---------------------------------
# AUTH
# ---------------------------------
require_user()

page_header(
    "Quiz Generator",
    "Generate quizzes from topics or PDF notes.",
    "📝"
)


# ---------------------------------
# SESSION STATE
# ---------------------------------
if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "answers" not in st.session_state:
    st.session_state.answers = {}


# ---------------------------------
# QUIZ MODE
# ---------------------------------
mode = st.radio(
    "Choose Quiz Mode",
    ["Topic Quiz", "PDF Quiz"]
)


# ==========================================================
# TOPIC QUIZ
# ==========================================================
if mode == "Topic Quiz":

    topic = st.text_input("Topic")

    col1, col2 = st.columns(2)

    with col1:
        num_questions = st.number_input(
            "Number of Questions",
            1,
            20,
            5
        )

    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"]
        )

    qtype = st.selectbox(
        "Question Type",
        ["MCQ", "True/False", "Short Answer"]
    )

    if st.button("🚀 Generate Topic Quiz"):

        if topic.strip() == "":
            st.warning("Enter a topic.")
            st.stop()

        with st.spinner("Generating quiz..."):

            quiz_data = generate_quiz(
                topic,
                num_questions,
                difficulty,
                qtype
            )

        if not quiz_data or "questions" not in quiz_data:
            st.error("Failed to generate quiz.")
            st.stop()

        st.session_state.quiz = quiz_data["questions"]
        st.session_state.answers = {}

        st.success("Quiz generated successfully!")


# ==========================================================
# PDF QUIZ
# ==========================================================
elif mode == "PDF Quiz":

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    col1, col2 = st.columns(2)

    with col1:
        num_questions = st.number_input(
            "Number of Questions",
            1,
            20,
            5,
            key="pdf_q"
        )

    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            key="pdf_d"
        )

    qtype = st.selectbox(
        "Question Type",
        ["MCQ", "True/False", "Short Answer"],
        key="pdf_type"
    )

    if st.button("🚀 Generate PDF Quiz"):

        if uploaded_file is None:
            st.warning("Please upload a PDF.")
            st.stop()

        with st.spinner("Reading PDF..."):
            text = load_pdf_text(uploaded_file)

        chunks = text.split("\n")
        chunks = [
            c.strip()
            for c in chunks
            if len(c.strip()) > 30
        ]

        context = "\n".join(chunks[:8])

        with st.spinner("Generating quiz..."):

            quiz_data = generate_quiz_from_context(
                context,
                num_questions,
                difficulty,
                qtype
            )

        if not quiz_data or "questions" not in quiz_data:
            st.error("Failed to generate quiz.")
            st.stop()

        st.session_state.quiz = quiz_data["questions"]
        st.session_state.answers = {}

        st.success("Quiz generated successfully!")


# ==========================================================
# DISPLAY QUIZ
# ==========================================================
if st.session_state.quiz:

    st.divider()

    st.subheader("📋 Your Quiz")

    for i, question in enumerate(st.session_state.quiz):

        st.markdown(
            f"### Q{i+1}. {question['question']}"
        )

        options = question.get("options", [])

        if options:

            answer = st.radio(
                "Choose an answer",
                options,
                key=f"ans_{i}"
            )

        else:

            answer = st.text_input(
                "Your Answer",
                key=f"ans_{i}"
            )

        st.session_state.answers[i] = answer

        st.write("---")


# ==========================================================
# SUBMIT QUIZ
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

        st.subheader("Review Answers")

        for result in results:

            if result["is_correct"]:
                st.success(result["question"])
            else:
                st.error(result["question"])

            st.write(
                f"**Correct Answer:** {result['correct_answer']}"
            )

            st.write(
                f"**Your Answer:** {result['user_answer']}"
            )

            st.write(
                f"**Explanation:** {result['explanation']}"
            )

            st.write("---")