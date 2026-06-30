from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config import GROQ_API_KEY, MODEL_NAME


# -----------------------------
# INIT LLM
# -----------------------------
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME,
)


# -----------------------------
# PROMPT
# -----------------------------
prompt = ChatPromptTemplate.from_template("""
You are SmartPrep AI, an expert academic planner.

Create a detailed, structured DAY-WISE study plan.

STUDENT DETAILS:
- Subjects: {subjects}
- Exam Date: {exam_date}
- Study Hours Per Day: {study_hours}
- Confidence Level: {confidence}
- Preferred Time: {preferred_time}

RULES:
- Give day-by-day plan
- Rotate subjects intelligently
- Balance revision, practice, learning
- Avoid repetition
- Make it realistic
- Keep output clean and structured

FORMAT:
Day 1:
- Time Slot:
- Subjects:
- Focus:
- Tasks:

Return clear structured output.
""")


# -----------------------------
# TIME SLOT GENERATOR
# -----------------------------
def generate_time_slots(preferred_time, study_hours):

    slots = {
        "Morning": "6:00 AM - 9:00 AM",
        "Afternoon": "2:00 PM - 5:00 PM",
        "Evening": "6:00 PM - 9:00 PM",
        "Night": "9:30 PM - 12:00 AM",
        "No Preference": "Flexible Time"
    }

    base_slot = slots.get(preferred_time, "Flexible Time")

    sessions = []
    remaining = study_hours

    while remaining > 0:
        if remaining >= 2:
            sessions.append("2-hour session")
            remaining -= 2
        else:
            sessions.append(f"{remaining}-hour session")
            remaining = 0

    return base_slot, sessions


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def generate_study_plan(
    education_level,
    course,
    subjects,
    exam_date,
    study_hours,
    preferred_time,
    remaining_days
):

    # format subjects for AI
    subject_text = "\n".join([
        f"- {s['subject']} | Priority: {s['priority']} | Difficulty: {s['difficulty']} | Scope: {s['scope']}"
        for s in subjects
    ])

    confidence = ", ".join(list(set([s["confidence"] for s in subjects])))

    base_slot, sessions = generate_time_slots(preferred_time, study_hours)

    formatted_prompt = prompt.format(
        subjects=subject_text,
        exam_date=str(exam_date),
        study_hours=study_hours,
        confidence=confidence,
        preferred_time=preferred_time
    )

    response = llm.invoke(formatted_prompt)

    return {
        "education_level": education_level,
        "course": course,
        "exam_date": str(exam_date),
        "remaining_days": remaining_days,
        "time_slot": base_slot,
        "sessions": sessions,
        "ai_plan": response.content
    }