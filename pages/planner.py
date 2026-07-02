import streamlit as st
from datetime import date

from agents.planner_agent import generate_study_plan
from utils.auth import require_user
from utils.ui_theme import page_header, section_title, ai_plan_card

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

st.set_page_config(page_title="Study Planner", page_icon="📅")

page_header(
    "Smart Study Planner",
    "Generate an AI-powered personalized study plan.",
    "📅"
)

# -------------------------------
# STUDENT INFO
# -------------------------------
section_title("Student Information", "🎓")

education_level = st.selectbox(
    "Education Level",
    [
        "Primary School",
        "High School",
        "PUC",
        "Undergraduate",
        "Postgraduate",
        "Competitive Exam",
        "Other"
    ]
)

course = st.text_input("Class / Course")

# -------------------------------
# PLANNING
# -------------------------------
section_title("Planning", "📅")

exam_date = st.date_input(
    "Exam Date",
    min_value=date.today()
)

study_hours = st.slider(
    "Study Hours Per Day",
    1,
    12,
    4
)

preferred_time = st.selectbox(
    "Preferred Study Time",
    [
        "Morning",
        "Afternoon",
        "Evening",
        "Night",
        "No Preference"
    ]
)

today = date.today()

remaining_days = (exam_date - today).days
available_hours = remaining_days * study_hours

st.info(f"""
📅 Today: **{today}**

🎯 Exam Date: **{exam_date}**

⏳ Days Left: **{remaining_days}**

📖 Total Study Hours: **{available_hours}**
""")

# -------------------------------
# SUBJECTS
# -------------------------------
section_title("Subjects", "📚")

number_of_subjects = st.number_input(
    "Number of Subjects",
    min_value=1,
    max_value=10,
    value=1
)

subjects = []

for i in range(number_of_subjects):

    st.subheader(f"Subject {i+1}")

    subject_name = st.text_input(
        "Subject Name",
        key=f"subject_{i}"
    )

    scope = st.selectbox(
        "Study Scope",
        [
            "Entire Subject",
            "Selected Chapters",
            "Specific Topics"
        ],
        key=f"scope_{i}"
    )

    chapters = ""
    topics = ""

    if scope == "Selected Chapters":
        chapters = st.text_area(
            "Chapters (one per line)",
            key=f"chapters_{i}"
        )

    elif scope == "Specific Topics":
        topics = st.text_area(
            "Topics (one per line)",
            key=f"topics_{i}"
        )

    confidence = st.select_slider(
        "Confidence",
        ["Low", "Medium", "High"],
        value="Medium",
        key=f"conf_{i}"
    )

    difficulty = st.select_slider(
        "Difficulty",
        ["Easy", "Medium", "Hard"],
        value="Medium",
        key=f"diff_{i}"
    )

    priority = st.select_slider(
        "Priority",
        ["Low", "Medium", "High"],
        value="Medium",
        key=f"prio_{i}"
    )

    subjects.append(
        {
            "subject": subject_name,
            "scope": scope,
            "chapters": chapters,
            "topics": topics,
            "confidence": confidence,
            "difficulty": difficulty,
            "priority": priority
        }
    )

st.divider()

# -------------------------------
# GENERATE PLAN
# -------------------------------

if st.button("🚀 Generate AI Study Plan"):

    if any(s["subject"].strip() == "" for s in subjects):
        st.error("Please enter all subject names.")

    elif remaining_days <= 0:
        st.error("Please select a future exam date.")

    else:

        with st.spinner("Generating your AI Study Plan..."):

            plan = generate_study_plan(
                education_level,
                course,
                subjects,
                exam_date,
                study_hours,
                preferred_time,
                remaining_days
            )

        st.success("Study Plan Generated Successfully!")

        section_title("Your AI Study Plan", "📊")

        ai_plan_card(
            plan["ai_plan"],
            plan["time_slot"],
            plan["sessions"]
        )