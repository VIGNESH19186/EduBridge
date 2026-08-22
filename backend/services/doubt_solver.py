"""
AI Doubt Solving Pipeline:

Student Question -> Classification (subject/topic/difficulty) -> RAG retrieval
-> Grounded explanation via AI service -> Citation generation -> Translation
"""
from typing import Dict
from sqlalchemy.orm import Session
from backend.services import rag_service
from backend.services.ai_service import ai_service
from backend.services.translation_service import translate_text

SUBJECT_KEYWORDS = {
    "Mathematics": ["equation", "algebra", "calculus", "derivative", "differentiat", "integral",
                    "integrat", "geometry", "fraction", "quadratic", "matrix", "probability",
                    "squared", "cubed", "x²", "x^2", "polynomial", "trigonometry", "logarithm"],
    "Physics": ["motion", "newton", "force", "velocity", "energy", "gravity", "friction", "wave"],
    "Chemistry": ["reaction", "molecule", "acid", "base", "compound", "element", "bond"],
    "Biology": ["cell", "photosynthesis", "organism", "gene", "ecosystem", "dna"],
    "Computer Science": ["algorithm", "function", "loop", "variable", "code", "array", "recursion"],
    "English": ["grammar", "essay", "sentence", "tense", "paragraph", "vocabulary"],
}

DIFFICULTY_KEYWORDS = {
    "advanced": ["prove", "derive", "optimi", "integral", "differential equation"],
    "beginner": ["what is", "define", "basic", "simple"],
}


def detect_subject(text: str) -> str:
    text_lower = text.lower()
    best_subject, best_hits = "General", 0
    for subject, keywords in SUBJECT_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in text_lower)
        if hits > best_hits:
            best_subject, best_hits = subject, hits
    return best_subject


def detect_topic(text: str, subject: str) -> str:
    text_lower = text.lower()
    if "differ" in text_lower or "derivative" in text_lower:
        return "Differential Calculus"
    if "quadratic" in text_lower:
        return "Quadratic Equations"
    if "newton" in text_lower or "force" in text_lower:
        return "Newton's Laws of Motion"
    if "fraction" in text_lower:
        return "Fractions"
    if "photosynthesis" in text_lower:
        return "Photosynthesis"
    if "algorithm" in text_lower or "loop" in text_lower:
        return "Algorithms & Control Flow"
    return f"General {subject}"


def detect_difficulty(text: str) -> str:
    text_lower = text.lower()
    for level, keywords in DIFFICULTY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return level
    return "intermediate"


def solve_doubt(db: Session, question_text: str, language: str = "English",
                 explanation_level: str = "intermediate") -> Dict:
    subject = detect_subject(question_text)
    topic = detect_topic(question_text, subject)
    difficulty = explanation_level or detect_difficulty(question_text)

    sources = rag_service.retrieve(db, question_text, top_k=3)
    grounded = len(sources) > 0

    if not grounded:
        explanation = rag_service.NO_GROUNDING_MESSAGE
        citations = []
    else:
        context_block = "\n\n".join(
            f"[Source: {s['title']} - {s['section']}]\n{s['content']}" for s in sources
        )
        system_prompt = (
            "You are EduBridge AI, a grounded educational tutor. Explain concepts "
            "step-by-step, matched to the student's level, using ONLY the provided "
            "sources as your factual grounding. Include: step-by-step breakdown, one "
            "worked example, a common mistake, and end with a 'Quick Check' question. "
            "Never fabricate facts or sources."
        )
        user_prompt = (
            f"Student level: {difficulty}\n"
            f"Sources:\n{context_block}\n\n"
            f"Student question: {question_text}"
        )
        explanation = ai_service.complete(system_prompt, user_prompt)
        citations = [
            {"title": s["title"], "section": s["section"], "source": s["source"] or "Open Educational Resource"}
            for s in sources
        ]

    if language and language != "English" and grounded:
        explanation = translate_text(explanation, language)

    quick_check = _generate_quick_check(topic)

    return {
        "detected_subject": subject,
        "detected_topic": topic,
        "detected_difficulty": difficulty,
        "explanation": explanation,
        "citations": citations,
        "quick_check_question": quick_check,
        "grounded": grounded,
        "language": language,
    }


def _generate_quick_check(topic: str) -> str:
    bank = {
        "Differential Calculus": "What is the derivative of x³?",
        "Quadratic Equations": "Solve: x² - 4x + 4 = 0",
        "Newton's Laws of Motion": "What happens to an object's velocity when no net force acts on it?",
        "Fractions": "Simplify: 8/12",
        "Photosynthesis": "Which gas do plants release during photosynthesis?",
        "Algorithms & Control Flow": "What is the time complexity of a single for-loop over n items?",
    }
    return bank.get(topic, "Can you summarize this concept in your own words?")
