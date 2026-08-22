"""
Simple evaluation harness for the doubt-solving pipeline's subject/topic
classification accuracy against ai/evaluation/test_questions.json.

Run with:
    python ai/evaluation/evaluate.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.services.doubt_solver import detect_subject, detect_topic  # noqa: E402


def run_evaluation():
    path = os.path.join(os.path.dirname(__file__), "test_questions.json")
    with open(path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    correct_subject, correct_topic = 0, 0
    for case in test_cases:
        subject = detect_subject(case["question"])
        topic = detect_topic(case["question"], subject)

        subject_match = subject == case["expected_subject"]
        topic_match = topic == case["expected_topic"]
        correct_subject += subject_match
        correct_topic += topic_match

        status = "✓" if subject_match and topic_match else "✗"
        print(f"{status} Q: {case['question']}")
        print(f"    Detected subject={subject} topic={topic}")
        print(f"    Expected subject={case['expected_subject']} topic={case['expected_topic']}")

    total = len(test_cases)
    print(f"\nSubject accuracy: {correct_subject}/{total}")
    print(f"Topic accuracy:   {correct_topic}/{total}")


if __name__ == "__main__":
    run_evaluation()
