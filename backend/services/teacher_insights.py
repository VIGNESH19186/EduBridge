"""
Teacher Insight Agent.

Generates risk assessments based ONLY on measurable learning data:
    - recent accuracy per topic
    - consecutive failed attempts
    - days since last activity

Never produces psychological or personal claims about the student -
only observable, data-backed statements and a concrete recommended action.
"""
import datetime
from typing import List, Dict
from sqlalchemy.orm import Session
from backend.models.student import Student
from backend.models.attempt import Attempt
from backend.models.recommendation import StudentProgress
from backend.models.user import User


def _days_since_last_activity(db: Session, student_id: int) -> int:
    last = (
        db.query(Attempt)
        .filter(Attempt.student_id == student_id)
        .order_by(Attempt.created_at.desc())
        .first()
    )
    if not last:
        return 999
    delta = datetime.datetime.utcnow() - last.created_at
    return delta.days


def _consecutive_failures(db: Session, student_id: int) -> int:
    attempts = (
        db.query(Attempt)
        .filter(Attempt.student_id == student_id)
        .order_by(Attempt.created_at.desc())
        .limit(5)
        .all()
    )
    streak = 0
    for a in attempts:
        if a.accuracy < 50:
            streak += 1
        else:
            break
    return streak


def get_students_needing_attention(db: Session, teacher_id: int) -> List[Dict]:
    students = db.query(Student).all()  # in a full multi-class impl, filter by teacher's classes
    results = []

    for student in students:
        progress = (
            db.query(StudentProgress)
            .filter(StudentProgress.student_id == student.id)
            .order_by(StudentProgress.mastery_percent.asc())
            .first()
        )
        if not progress:
            continue

        weak_topic = progress.topic.name if progress.topic else "General"
        accuracy = progress.accuracy_percent
        inactivity_days = _days_since_last_activity(db, student.id)
        fail_streak = _consecutive_failures(db, student.id)

        evidence = []
        risk_score = 0

        if accuracy < 50:
            evidence.append(f"{weak_topic} accuracy: {accuracy:.0f}%")
            risk_score += 2
        if fail_streak >= 3:
            evidence.append(f"{fail_streak} consecutive failed attempts")
            risk_score += 2
        if inactivity_days >= 5:
            evidence.append(f"No practice activity for {inactivity_days} days")
            risk_score += 1

        if risk_score == 0:
            continue

        risk_level = "HIGH" if risk_score >= 4 else "MEDIUM" if risk_score >= 2 else "LOW"
        user = db.query(User).filter(User.id == student.user_id).first()

        results.append(
            {
                "student_id": student.id,
                "student_name": user.name if user else "Unknown",
                "risk_level": risk_level,
                "evidence": evidence,
                "weak_topic": weak_topic,
                "recommended_intervention": f"Assign beginner-level {weak_topic} practice.",
            }
        )

    results.sort(key=lambda r: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[r["risk_level"]])
    return results
