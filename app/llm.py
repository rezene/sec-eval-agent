"""Swappable LLM interface so the agent doesn't depend on one provider/SDK."""

from abc import ABC, abstractmethod

from app.config import settings


class LLMClient(ABC):
    @abstractmethod
    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Return a raw text completion for the given prompts."""


class OpenAIClient(LLMClient):
    def __init__(self, model: str | None = None):
        from openai import OpenAI

        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = model or settings.llm_model

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""


def get_llm_client() -> LLMClient:
    if settings.llm_provider == "openai":
        return OpenAIClient()
    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
