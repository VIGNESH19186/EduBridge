from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    question_type = Column(String(20), default="mcq")  # mcq | short_answer | numerical
    prompt = Column(Text, nullable=False)
    options = Column(Text, default="[]")  # JSON-encoded list for MCQ
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text, default="")
    difficulty = Column(String(20), default="beginner")

    topic = relationship("Topic", back_populates="questions")
