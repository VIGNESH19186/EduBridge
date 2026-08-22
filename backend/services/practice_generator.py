"""
Adaptive Practice Generator.

Rule:
    accuracy > 80%   -> increase difficulty
    accuracy 50-80%  -> maintain difficulty
    accuracy < 50%   -> reduce difficulty / foundational practice
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.question import Question
from backend.models.topic import Topic
from backend.models.attempt import Attempt


DIFFICULTY_ORDER = ["beginner", "intermediate", "advanced"]


def next_difficulty(current: str, accuracy: float) -> str:
    idx = DIFFICULTY_ORDER.index(current) if current in DIFFICULTY_ORDER else 0
    if accuracy > 80 and idx < len(DIFFICULTY_ORDER) - 1:
        return DIFFICULTY_ORDER[idx + 1]
    if accuracy < 50 and idx > 0:
        return DIFFICULTY_ORDER[idx - 1]
    return DIFFICULTY_ORDER[idx]


def get_recent_accuracy(db: Session, student_id: int, topic_name: Optional[str] = None) -> float:
    query = db.query(Attempt).filter(Attempt.student_id == student_id)
    attempts = query.order_by(Attempt.created_at.desc()).limit(5).all()
    if not attempts:
        return 60.0  # neutral default for new students
    return sum(a.accuracy for a in attempts) / len(attempts)


def generate_practice(db: Session, student_id: int, subject: Optional[str] = None,
                       topic: Optional[str] = None, count: int = 5) -> List[Question]:
    accuracy = get_recent_accuracy(db, student_id, topic)
    difficulty = next_difficulty("beginner", accuracy)

    query = db.query(Question).join(Topic)
    if topic:
        query = query.filter(Topic.name.ilike(f"%{topic}%"))
    if subject:
        query = query.join(Topic.subject).filter(Topic.subject.has(name=subject))

    questions = query.filter(Question.difficulty == difficulty).limit(count).all()
    if len(questions) < count:
        # fill remaining slots from any difficulty for the topic
        extra = query.limit(count - len(questions)).all()
        seen_ids = {q.id for q in questions}
        questions += [q for q in extra if q.id not in seen_ids]

    return questions[:count]
