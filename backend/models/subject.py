from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(String(255), default="")

    topics = relationship("Topic", back_populates="subject")
