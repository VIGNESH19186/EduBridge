import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from backend.database.database import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    score_percent = Column(Float, default=0.0)
    accuracy = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="attempts")
    answers = relationship("Answer", back_populates="attempt")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    given_answer = Column(String(255), default="")
    is_correct = Column(Boolean, default=False)

    attempt = relationship("Attempt", back_populates="answers")
    question = relationship("Question")
