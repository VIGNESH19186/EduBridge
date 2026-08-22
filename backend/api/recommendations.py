from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.api.auth import require_role
from backend.models.user import User
from backend.models.student import Student
from backend.services.recommendation_engine import build_recommendations

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("")
def get_recommendations(db: Session = Depends(get_db), user: User = Depends(require_role("student"))):
    student = db.query(Student).filter(Student.user_id == user.id).first()
    return build_recommendations(db, student.id)
