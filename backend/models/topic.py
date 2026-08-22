from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    difficulty = Column(String(20), default="beginner")

    subject = relationship("Subject", back_populates="topics")
    questions = relationship("Question", back_populates="topic")
