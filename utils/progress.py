import json
import os

PROGRESS_FILE = "data/progress.json"


def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}

    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=4)


def update_progress(subject, task, completed):
    progress = load_progress()

    if subject not in progress:
        progress[subject] = {}

    progress[subject][task] = completed

    save_progress(progress)


def calculate_progress():
    progress = load_progress()

    total = 0
    completed = 0

    for subject in progress.values():
        for task in subject.values():
            total += 1

            if task:
                completed += 1

    if total == 0:
        return 0

    return round((completed / total) * 100)