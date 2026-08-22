from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(180), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    difficulty = Column(String(20), default="beginner")
    time_limit_minutes = Column(Integer, default=15)
    created_by_teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)

    subject = relationship("Subject")
    topic = relationship("Topic")
    quiz_questions = relationship("QuizQuestion", back_populates="quiz")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    quiz = relationship("Quiz", back_populates="quiz_questions")
    question = relationship("Question")
