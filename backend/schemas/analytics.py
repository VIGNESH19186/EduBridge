from pydantic import BaseModel
from typing import List


class TopicMasteryOut(BaseModel):
    topic: str
    mastery_percent: float


class WeeklyActivityOut(BaseModel):
    day: str
    questions_solved: int


class AnalyticsOut(BaseModel):
    subject_mastery: List[TopicMasteryOut]
    topic_performance: List[TopicMasteryOut]
    weekly_activity: List[WeeklyActivityOut]
    quiz_accuracy: float
