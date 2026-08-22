from pydantic import BaseModel
from typing import List


class WeakTopicOut(BaseModel):
    topic: str
    mastery_percent: float


class StudentProfileOut(BaseModel):
    id: int
    name: str
    grade_level: str
    learning_streak_days: int
    overall_mastery: float
    questions_solved: int
    accuracy: float
    weak_topics: List[WeakTopicOut]


class RecommendationOut(BaseModel):
    topic_name: str
    reason: str
    difficulty: str
    estimated_minutes: int
