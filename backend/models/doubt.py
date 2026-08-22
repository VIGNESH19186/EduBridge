import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from backend.database.database import Base


class Doubt(Base):
    __tablename__ = "doubts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    detected_subject = Column(String(100), default="")
    detected_topic = Column(String(150), default="")
    detected_difficulty = Column(String(20), default="beginner")
    language = Column(String(20), default="English")
    explanation = Column(Text, default="")
    citations = Column(Text, default="[]")  # JSON list
    grounded = Column(String(10), default="true")  # "true"/"false" string flag
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="doubts")
