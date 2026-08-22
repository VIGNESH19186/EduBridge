from pydantic import BaseModel
from typing import List, Optional


class PracticeGenerateRequest(BaseModel):
    subject: Optional[str] = None
    topic: Optional[str] = None
    count: int = 5


class PracticeQuestionOut(BaseModel):
    id: int
    prompt: str
    options: List[str]
    difficulty: str
    topic: str


class PracticeSubmitAnswer(BaseModel):
    question_id: int
    given_answer: str


class PracticeSubmitRequest(BaseModel):
    answers: List[PracticeSubmitAnswer]
    topic: Optional[str] = None


class PracticeResultItem(BaseModel):
    question_id: int
    is_correct: bool
    correct_answer: str
    explanation: str


class PracticeSubmitResponse(BaseModel):
    score_percent: float
    accuracy: float
    results: List[PracticeResultItem]
    new_difficulty_recommendation: str
