import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.api.auth import require_role
from backend.models.user import User
from backend.models.student import Student
from backend.models.doubt import Doubt
from backend.schemas.doubt import DoubtRequest, DoubtResponse, CitationOut
from backend.services.doubt_solver import solve_doubt

router = APIRouter(prefix="/api/doubts", tags=["doubts"])


@router.post("", response_model=DoubtResponse)
def ask_doubt(payload: DoubtRequest, db: Session = Depends(get_db),
              user: User = Depends(require_role("student"))):
    student = db.query(Student).filter(Student.user_id == user.id).first()

    result = solve_doubt(
        db,
        question_text=payload.question_text,
        language=payload.language or user.preferred_language,
        explanation_level=payload.explanation_level,
    )

    doubt = Doubt(
        student_id=student.id,
        question_text=payload.question_text,
        detected_subject=result["detected_subject"],
        detected_topic=result["detected_topic"],
        detected_difficulty=result["detected_difficulty"],
        language=result["language"],
        explanation=result["explanation"],
        citations=json.dumps(result["citations"]),
        grounded="true" if result["grounded"] else "false",
    )
    db.add(doubt)
    db.commit()
    db.refresh(doubt)

    return DoubtResponse(
        id=doubt.id,
        detected_subject=result["detected_subject"],
        detected_topic=result["detected_topic"],
        detected_difficulty=result["detected_difficulty"],
        explanation=result["explanation"],
        citations=[CitationOut(**c) for c in result["citations"]],
        quick_check_question=result["quick_check_question"],
        grounded=result["grounded"],
        language=result["language"],
    )


@router.get("/history")
def doubt_history(db: Session = Depends(get_db), user: User = Depends(require_role("student"))):
    student = db.query(Student).filter(Student.user_id == user.id).first()
    doubts = (
        db.query(Doubt)
        .filter(Doubt.student_id == student.id)
        .order_by(Doubt.created_at.desc())
        .all()
    )
    return [
        {
            "id": d.id,
            "question_text": d.question_text,
            "detected_subject": d.detected_subject,
            "detected_topic": d.detected_topic,
            "created_at": d.created_at.isoformat(),
            "grounded": d.grounded == "true",
        }
        for d in doubts
    ]
