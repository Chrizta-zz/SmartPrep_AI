import streamlit as st
from datetime import date

from agents.planner_agent import generate_study_plan
from utils.auth import require_login

require_login()

st.set_page_config(page_title="Study Planner", page_icon="📅")

st.title("📅 SmartPrep AI - Smart Study Planner")
st.write("Generate an AI-powered personalized study plan.")

# -------------------------------
# STUDENT INFO
# -------------------------------
st.header("🎓 Student Information")

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
st.header("📅 Planning")

exam_date = st.date_input("Exam Date", min_value=date.today())

study_hours = st.slider("Study Hours Per Day", 1, 12, 4)

preferred_time = st.selectbox(
    "Preferred Study Time",
    ["Morning", "Afternoon", "Evening", "Night", "No Preference"]
)

today = date.today()
remaining_days = (exam_date - today).days
available_hours = remaining_days * study_hours

st.info(f"""
📅 Today: **{today}**  
🎯 Exam Date: **{exam_date}**  
⏳ Days Left: **{remaining_days}**  
📖 Total Hours: **{available_hours}**
""")

# -------------------------------
# SUBJECTS
# -------------------------------
st.header("📚 Subjects")

number_of_subjects = st.number_input("Number of Subjects", 1, 10, 1)

subjects = []

for i in range(number_of_subjects):

    st.subheader(f"Subject {i+1}")

    subject_name = st.text_input("Subject Name", key=f"subject_{i}")

    scope = st.selectbox(
        "Study Scope",
        ["Entire Subject", "Selected Chapters", "Specific Topics"],
        key=f"scope_{i}"
    )

    chapters = ""
    topics = ""

    if scope == "Selected Chapters":
        chapters = st.text_area("Chapters (one per line)", key=f"chapters_{i}")

    elif scope == "Specific Topics":
        topics = st.text_area("Topics (one per line)", key=f"topics_{i}")

    confidence = st.select_slider("Confidence", ["Low", "Medium", "High"], value="Medium", key=f"conf_{i}")
    difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"], value="Medium", key=f"diff_{i}")
    priority = st.select_slider("Priority", ["Low", "Medium", "High"], value="Medium", key=f"prio_{i}")

    subjects.append({
        "subject": subject_name,
        "scope": scope,
        "chapters": chapters,
        "topics": topics,
        "confidence": confidence,
        "difficulty": difficulty,
        "priority": priority
    })

st.divider()

# -------------------------------
# GENERATE PLAN
# -------------------------------
if st.button("🚀 Generate AI Study Plan"):

    # validations
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

        # -------------------------------
        # OUTPUT SECTION (FIXED)
        # -------------------------------
        st.subheader("📊 Your AI Study Plan")

        # TIME INFO
        st.markdown(f"""
        🕒 **Time Slot:** {plan['time_slot']}  
        ⏱ **Sessions:** {', '.join(plan['sessions'])}
        """)

        st.markdown("---")

        # AI GENERATED OUTPUT
        st.markdown("## 🤖 AI Generated Schedule")

        st.markdown(plan["ai_plan"])