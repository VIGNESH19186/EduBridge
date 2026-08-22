"""
AI Service abstraction layer.

Supports a configurable LLM provider via environment variables:
    AI_PROVIDER, AI_API_KEY, AI_MODEL

If AI_API_KEY is not set, the service automatically runs in DEMO MODE,
returning clearly-labeled, deterministic sample content so the rest of the
platform (RAG, citations, adaptive practice, analytics) remains fully
functional and demonstrable without any paid API access.
"""
import httpx
from backend.config import settings
from backend.utils.logging import logger


class AIService:
    def __init__(self):
        self.provider = settings.ai_provider
        self.api_key = settings.ai_api_key
        self.model = settings.ai_model
        self.demo_mode = settings.demo_mode

    def is_demo(self) -> bool:
        return self.demo_mode

    def complete(self, system_prompt: str, user_prompt: str, max_tokens: int = 800) -> str:
        """
        Send a prompt to the configured LLM provider and return plain text.
        Falls back to a demo-mode response if no API key is configured or
        if the live call fails for any reason (network, quota, etc.).
        """
        if self.demo_mode:
            return self._demo_response(user_prompt)

        try:
            if self.provider == "anthropic":
                return self._call_anthropic(system_prompt, user_prompt, max_tokens)
            else:
                logger.warning(f"Unknown AI_PROVIDER '{self.provider}', falling back to demo mode.")
                return self._demo_response(user_prompt)
        except Exception as exc:  # noqa: broad-except intentional: never crash the UX
            logger.error(f"AI provider call failed, falling back to demo mode: {exc}")
            return self._demo_response(user_prompt)

    def _call_anthropic(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        parts = [block["text"] for block in data.get("content", []) if block.get("type") == "text"]
        return "\n".join(parts).strip()

    @staticmethod
    def _demo_response(user_prompt: str) -> str:
        return (
            "[DEMO MODE RESPONSE]\n"
            "This is a sample explanation generated without a live AI provider "
            "connected. Configure AI_API_KEY in your .env file to enable live "
            "AI-generated explanations.\n\n"
            f"Your question was: {user_prompt[:200]}"
        )


ai_service = AIService()
