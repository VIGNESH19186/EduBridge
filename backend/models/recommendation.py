import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from backend.database.database import Base


class StudentProgress(Base):
    __tablename__ = "student_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    mastery_percent = Column(Float, default=0.0)
    accuracy_percent = Column(Float, default=0.0)
    questions_solved = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="progress_records")
    subject = relationship("Subject")
    topic = relationship("Topic")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic_name = Column(String(150), nullable=False)
    reason = Column(Text, default="")
    difficulty = Column(String(20), default="beginner")
    estimated_minutes = Column(Integer, default=15)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="recommendations")
