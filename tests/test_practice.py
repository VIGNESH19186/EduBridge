import json
import os
from tests.conftest import register_and_login
from backend.database.database import SessionLocal
from backend.models.subject import Subject
from backend.models.topic import Topic
from backend.models.question import Question
from backend.services.practice_generator import next_difficulty


def _seed_topic_with_questions():
    db = SessionLocal()
    try:
        unique_suffix = os.urandom(4).hex()
        subject = Subject(name=f"Test Subject {unique_suffix}")
        db.add(subject)
        db.flush()
        topic = Topic(name=f"Test Topic {unique_suffix}", subject_id=subject.id, difficulty="beginner")
        db.add(topic)
        db.flush()
        for i in range(3):
            db.add(Question(
                topic_id=topic.id, question_type="mcq",
                prompt=f"Sample question {i}?",
                options=json.dumps(["A", "B", "C", "D"]),
                correct_answer="A", explanation="Because A is correct.",
                difficulty="beginner",
            ))
        db.commit()
        return topic.name
    finally:
        db.close()


def test_adaptive_difficulty_rules():
    assert next_difficulty("beginner", 90) == "intermediate"
    assert next_difficulty("intermediate", 60) == "intermediate"
    assert next_difficulty("intermediate", 30) == "beginner"
    assert next_difficulty("advanced", 95) == "advanced"  # already at ceiling


def test_generate_practice_returns_questions(client):
    topic_name = _seed_topic_with_questions()
    data = register_and_login(client, "student", email="practicestudent@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    resp = client.post("/api/practice/generate", json={"topic": topic_name, "count": 3}, headers=headers)
    assert resp.status_code == 200
    questions = resp.json()
    assert len(questions) > 0
    assert questions[0]["topic"] == topic_name


def test_submit_practice_scores_and_updates_progress(client):
    topic_name = _seed_topic_with_questions()
    data = register_and_login(client, "student", email="submitstudent@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    questions = client.post(
        "/api/practice/generate", json={"topic": topic_name, "count": 3}, headers=headers
    ).json()

    answers = [{"question_id": q["id"], "given_answer": "A"} for q in questions]
    resp = client.post("/api/practice/submit", json={"answers": answers}, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["score_percent"] == 100.0
    assert body["new_difficulty_recommendation"] in ("beginner", "intermediate", "advanced")
