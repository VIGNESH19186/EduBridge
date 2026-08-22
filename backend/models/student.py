from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.database.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    grade_level = Column(String(20), default="Grade 10")
    learning_streak_days = Column(Integer, default=0)

    user = relationship("User", back_populates="student_profile")
    doubts = relationship("Doubt", back_populates="student")
    attempts = relationship("Attempt", back_populates="student")
    progress_records = relationship("StudentProgress", back_populates="student")
    recommendations = relationship("Recommendation", back_populates="student")
    class_memberships = relationship("ClassMember", back_populates="student")
