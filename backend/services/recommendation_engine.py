"""
Recommendation Engine.

Builds a personalized learning path from a student's measured progress
records: lowest-mastery topics first, with a plain-language reason,
recommended difficulty, and estimated time.
"""
from typing import List, Dict
from sqlalchemy.orm import Session
from backend.models.recommendation import StudentProgress


def build_recommendations(db: Session, student_id: int, limit: int = 4) -> List[Dict]:
    records = (
        db.query(StudentProgress)
        .filter(StudentProgress.student_id == student_id)
        .order_by(StudentProgress.mastery_percent.asc())
        .limit(limit)
        .all()
    )

    recs = []
    for r in records:
        topic_name = r.topic.name if r.topic else "General Review"
        if r.mastery_percent < 50:
            reason = f"Your recent accuracy is {r.accuracy_percent:.0f}%. Foundational practice recommended."
            difficulty = "beginner"
            minutes = 20
        elif r.mastery_percent < 75:
            reason = "Practice recommended to solidify this topic."
            difficulty = "intermediate"
            minutes = 15
        else:
            reason = "You're ready for more advanced problems here."
            difficulty = "advanced"
            minutes = 10

        recs.append(
            {
                "topic_name": topic_name,
                "reason": reason,
                "difficulty": difficulty,
                "estimated_minutes": minutes,
            }
        )
    return recs
