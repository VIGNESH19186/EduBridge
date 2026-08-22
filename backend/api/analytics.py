import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.api.auth import require_role
from backend.models.user import User
from backend.models.student import Student
from backend.models.recommendation import StudentProgress
from backend.models.attempt import Attempt
from backend.schemas.analytics import AnalyticsOut, TopicMasteryOut, WeeklyActivityOut

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/student", response_model=AnalyticsOut)
def student_analytics(db: Session = Depends(get_db), user: User = Depends(require_role("student"))):
    student = db.query(Student).filter(Student.user_id == user.id).first()
    progress = db.query(StudentProgress).filter(StudentProgress.student_id == student.id).all()

    subject_mastery: dict[str, list[float]] = {}
    for p in progress:
        name = p.subject.name if p.subject else "General"
        subject_mastery.setdefault(name, []).append(p.mastery_percent)

    subject_out = [
        TopicMasteryOut(topic=name, mastery_percent=round(sum(v) / len(v), 1))
        for name, v in subject_mastery.items()
    ]
    topic_out = [
        TopicMasteryOut(topic=p.topic.name if p.topic else "General", mastery_percent=p.mastery_percent)
        for p in progress
    ]

    attempts = db.query(Attempt).filter(Attempt.student_id == student.id).all()
    quiz_accuracy = round(sum(a.accuracy for a in attempts) / len(attempts), 1) if attempts else 0.0

    weekly = []
    today = datetime.datetime.utcnow().date()
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        count = sum(1 for a in attempts if a.created_at.date() == day)
        weekly.append(WeeklyActivityOut(day=day.strftime("%a"), questions_solved=count))

    return AnalyticsOut(
        subject_mastery=subject_out,
        topic_performance=topic_out,
        weekly_activity=weekly,
        quiz_accuracy=quiz_accuracy,
    )
