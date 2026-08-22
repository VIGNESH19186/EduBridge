from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.api.auth import require_role
from backend.models.user import User
from backend.models.teacher import Teacher
from backend.models.student import Student
from backend.models.recommendation import StudentProgress
from backend.schemas.teacher import StudentAttentionOut, TeacherDashboardOut
from backend.services.teacher_insights import get_students_needing_attention

router = APIRouter(prefix="/api/teachers", tags=["teachers"])


def _get_teacher(db: Session, user: User) -> Teacher:
    teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
    if not teacher:
        if user.role.value == "admin":
            return Teacher(id=0, user_id=user.id)  # admins view platform-wide, unbound to a teacher record
        raise HTTPException(status_code=404, detail="Teacher profile not found.")
    return teacher


@router.get("/dashboard", response_model=TeacherDashboardOut)
def dashboard(db: Session = Depends(get_db), user: User = Depends(require_role("teacher", "admin"))):
    teacher = _get_teacher(db, user)
    total_students = db.query(Student).count()
    progress_records = db.query(StudentProgress).all()
    class_average = (
        sum(p.mastery_percent for p in progress_records) / len(progress_records)
        if progress_records else 0.0
    )
    attention_list = get_students_needing_attention(db, teacher.id)
    weak_topics = {r["weak_topic"] for r in attention_list}

    return TeacherDashboardOut(
        total_students=total_students,
        class_average=round(class_average, 1),
        students_needing_attention=len(attention_list),
        topics_needing_review=len(weak_topics),
    )


@router.get("/students")
def list_students(db: Session = Depends(get_db), user: User = Depends(require_role("teacher", "admin"))):
    students = db.query(Student).all()
    return [
        {
            "student_id": s.id,
            "name": s.user.name if s.user else "Unknown",
            "grade_level": s.grade_level,
        }
        for s in students
    ]


@router.get("/insights", response_model=list[StudentAttentionOut])
def insights(db: Session = Depends(get_db), user: User = Depends(require_role("teacher", "admin"))):
    teacher = _get_teacher(db, user)
    return get_students_needing_attention(db, teacher.id)
