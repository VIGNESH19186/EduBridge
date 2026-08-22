from pydantic import BaseModel, Field
from typing import Optional, List


class DoubtRequest(BaseModel):
    question_text: str = Field(..., min_length=3)
    subject_hint: Optional[str] = None
    language: Optional[str] = "English"
    explanation_level: Optional[str] = "intermediate"  # simpler | intermediate | advanced


class CitationOut(BaseModel):
    title: str
    section: str
    source: str


class DoubtResponse(BaseModel):
    id: int
    detected_subject: str
    detected_topic: str
    detected_difficulty: str
    explanation: str
    citations: List[CitationOut]
    quick_check_question: str
    grounded: bool
    language: str

    class Config:
        from_attributes = True
