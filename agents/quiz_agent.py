import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)


# =========================================================
# 🟢 1. TOPIC-BASED QUIZ GENERATION
# =========================================================
def generate_quiz(topic: str, num_questions: int, difficulty: str, qtype: str):

    prompt = f"""
You are an expert quiz generator.

Generate a quiz in STRICT JSON format only.

Topic: {topic}
Number of Questions: {num_questions}
Difficulty: {difficulty}
Question Type: {qtype}

Rules:
- Output ONLY valid JSON (no markdown, no explanation)
- Each question must have:
  - question
  - options (4 for MCQ, ["True","False"] for TF, [] for short answer)
  - answer
  - explanation

Return format:
{{
  "questions": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "explanation": "..."
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You generate structured quizzes only in JSON format."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        return {"questions": []}


# =========================================================
# 🔵 2. RAG / PDF-BASED QUIZ GENERATION
# =========================================================
def generate_quiz_from_context(context: str, num_questions: int, difficulty: str, qtype: str):

    prompt = f"""
You are an expert quiz generator.

Generate a quiz ONLY from the given context.

CONTEXT:
{context}

Rules:
- Use ONLY the provided context (no outside knowledge)
- Output STRICT JSON only
- {num_questions} questions
- Difficulty: {difficulty}
- Type: {qtype}

Each question must include:
- question
- options
- answer
- explanation

Return format:
{{
  "questions": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "explanation": "based on context"
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You generate quizzes strictly from given context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        return {"questions": []}