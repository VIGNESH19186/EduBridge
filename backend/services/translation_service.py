"""
Translation service. Uses the configured AI provider to translate grounded
explanations into the student's selected language while preserving meaning.
In demo mode, returns a clearly-labeled note instead of a fabricated
translation, since we cannot guarantee translation quality without a live model.
"""
from backend.services.ai_service import ai_service

SUPPORTED_LANGUAGES = ["English", "हिन्दी", "ಕನ್ನಡ", "தமிழ்", "తెలుగు"]


def translate_text(text: str, target_language: str) -> str:
    if target_language == "English" or target_language not in SUPPORTED_LANGUAGES:
        return text

    if ai_service.is_demo():
        return (
            f"{text}\n\n[DEMO MODE: Translation to {target_language} requires a "
            f"live AI_API_KEY. Showing original English explanation.]"
        )

    system_prompt = (
        f"Translate the following educational explanation into {target_language}. "
        "Preserve all mathematical notation, step numbering, and meaning exactly."
    )
    return ai_service.complete(system_prompt, text)
