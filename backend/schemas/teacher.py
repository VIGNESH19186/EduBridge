from pydantic import BaseModel
from typing import List


class StudentAttentionOut(BaseModel):
    student_id: int
    student_name: str
    risk_level: str  # HIGH | MEDIUM | LOW
    evidence: List[str]
    weak_topic: str
    recommended_intervention: str


class TeacherDashboardOut(BaseModel):
    total_students: int
    class_average: float
    students_needing_attention: int
    topics_needing_review: int
