from pydantic import BaseModel
from typing import List, Optional


class QuizQuestionIn(BaseModel):
    question_type: str = "mcq"
    prompt: str
    options: List[str] = []
    correct_answer: str
    explanation: Optional[str] = ""
    difficulty: str = "beginner"


class QuizCreateRequest(BaseModel):
    title: str
    subject: str
    topic: str
    difficulty: str = "beginner"
    time_limit_minutes: int = 15
    questions: List[QuizQuestionIn]


class QuizOut(BaseModel):
    id: int
    title: str
    difficulty: str
    time_limit_minutes: int
    question_count: int
