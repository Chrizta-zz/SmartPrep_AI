# utils/quiz_parser.py

def evaluate_quiz(questions, user_answers):
    correct = 0
    results = []

    for i, q in enumerate(questions):
        correct_answer = q["answer"]
        user_answer = user_answers.get(i)

        is_correct = user_answer == correct_answer

        if is_correct:
            correct += 1

        results.append({
            "question": q["question"],
            "correct_answer": correct_answer,
            "user_answer": user_answer,
            "is_correct": is_correct,
            "explanation": q.get("explanation", "")
        })

    total = len(questions)
    accuracy = (correct / total) * 100 if total > 0 else 0

    return correct, total, accuracy, results