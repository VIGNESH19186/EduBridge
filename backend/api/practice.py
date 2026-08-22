import json
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.api.auth import require_role
from backend.models.user import User
from backend.models.student import Student
from backend.models.question import Question
from backend.models.attempt import Attempt, Answer
from backend.models.recommendation import StudentProgress
from backend.schemas.practice import (
    PracticeGenerateRequest, PracticeQuestionOut,
    PracticeSubmitRequest, PracticeSubmitResponse, PracticeResultItem,
)
from backend.services.practice_generator import generate_practice, next_difficulty

router = APIRouter(prefix="/api/practice", tags=["practice"])


@router.post("/generate", response_model=list[PracticeQuestionOut])
def practice_generate(payload: PracticeGenerateRequest, db: Session = Depends(get_db),
                       user: User = Depends(require_role("student"))):
    student = db.query(Student).filter(Student.user_id == user.id).first()
    questions = generate_practice(db, student.id, payload.subject, payload.topic, payload.count)
    return [
        PracticeQuestionOut(
            id=q.id,
            prompt=q.prompt,
            options=json.loads(q.options or "[]"),
            difficulty=q.difficulty,
            topic=q.topic.name if q.topic else "General",
        )
        for q in questions
    ]


@router.post("/submit", response_model=PracticeSubmitResponse)
def practice_submit(payload: PracticeSubmitRequest, db: Session = Depends(get_db),
                     user: User = Depends(require_role("student"))):
    student = db.query(Student).filter(Student.user_id == user.id).first()
    if not payload.answers:
        raise HTTPException(status_code=400, detail="No answers submitted.")

    results = []
    correct_count = 0
    topic_obj = None

    attempt = Attempt(student_id=student.id, score_percent=0, accuracy=0)
    db.add(attempt)
    db.flush()

    for ans in payload.answers:
        question = db.query(Question).filter(Question.id == ans.question_id).first()
        if not question:
            continue
        topic_obj = question.topic
        is_correct = ans.given_answer.strip().lower() == question.correct_answer.strip().lower()
        if is_correct:
            correct_count += 1

        db.add(Answer(
            attempt_id=attempt.id,
            question_id=question.id,
            given_answer=ans.given_answer,
            is_correct=is_correct,
        ))
        results.append(PracticeResultItem(
            question_id=question.id,
            is_correct=is_correct,
            correct_answer=question.correct_answer,
            explanation=question.explanation,
        ))

    total = len(payload.answers)
    accuracy = round((correct_count / total) * 100, 1) if total else 0.0
    attempt.score_percent = accuracy
    attempt.accuracy = accuracy
    attempt.topic_id = topic_obj.id if topic_obj else None

    # Update / create student progress for this topic
    if topic_obj:
        progress = (
            db.query(StudentProgress)
            .filter(StudentProgress.student_id == student.id, StudentProgress.topic_id == topic_obj.id)
            .first()
        )
        if not progress:
            progress = StudentProgress(
                student_id=student.id,
                subject_id=topic_obj.subject_id,
                topic_id=topic_obj.id,
                mastery_percent=accuracy,
                accuracy_percent=accuracy,
                questions_solved=total,
            )
            db.add(progress)
        else:
            progress.questions_solved += total
            progress.accuracy_percent = accuracy
            # mastery moves toward accuracy gradually (simple smoothing)
            progress.mastery_percent = round((progress.mastery_percent * 0.6) + (accuracy * 0.4), 1)
            progress.last_updated = datetime.datetime.utcnow()

    db.commit()

    current_difficulty = topic_obj.difficulty if topic_obj else "beginner"
    new_difficulty = next_difficulty(current_difficulty, accuracy)

    return PracticeSubmitResponse(
        score_percent=accuracy,
        accuracy=accuracy,
        results=results,
        new_difficulty_recommendation=new_difficulty,
    )
