from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.api.auth import require_role
from backend.models.user import User
from backend.models.student import Student
from backend.models.recommendation import StudentProgress
from backend.models.attempt import Attempt
from backend.schemas.student import StudentProfileOut, WeakTopicOut

router = APIRouter(prefix="/api/students", tags=["students"])


def _get_student(db: Session, user: User) -> Student:
    student = db.query(Student).filter(Student.user_id == user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")
    return student


@router.get("/me", response_model=StudentProfileOut)
def get_my_profile(db: Session = Depends(get_db), user: User = Depends(require_role("student"))):
    student = _get_student(db, user)
    progress_records = db.query(StudentProgress).filter(StudentProgress.student_id == student.id).all()

    overall_mastery = (
        sum(p.mastery_percent for p in progress_records) / len(progress_records)
        if progress_records else 0.0
    )
    questions_solved = sum(p.questions_solved for p in progress_records)
    accuracy = (
        sum(p.accuracy_percent for p in progress_records) / len(progress_records)
        if progress_records else 0.0
    )
    weak_topics = [
        WeakTopicOut(topic=p.topic.name if p.topic else "General", mastery_percent=p.mastery_percent)
        for p in sorted(progress_records, key=lambda p: p.mastery_percent)[:3]
    ]

    return StudentProfileOut(
        id=student.id,
        name=user.name,
        grade_level=student.grade_level,
        learning_streak_days=student.learning_streak_days,
        overall_mastery=round(overall_mastery, 1),
        questions_solved=questions_solved,
        accuracy=round(accuracy, 1),
        weak_topics=weak_topics,
    )


@router.get("/progress")
def get_progress(db: Session = Depends(get_db), user: User = Depends(require_role("student"))):
    student = _get_student(db, user)
    records = db.query(StudentProgress).filter(StudentProgress.student_id == student.id).all()
    return [
        {
            "subject": r.subject.name if r.subject else "General",
            "topic": r.topic.name if r.topic else "General",
            "mastery_percent": r.mastery_percent,
            "accuracy_percent": r.accuracy_percent,
            "questions_solved": r.questions_solved,
        }
        for r in records
    ]
