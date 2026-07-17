from config import (
    GEMINI,
    LLM_PROVIDER,
    OPENROUTER,
)

from .base import BaseLLMClient
from .gemini_client import GeminiClient
from .openrouter_client import OpenRouterClient


class LLMFactory:

    @staticmethod
    def create() -> BaseLLMClient:

        if LLM_PROVIDER == GEMINI:
            return GeminiClient()

        if LLM_PROVIDER == OPENROUTER:
            return OpenRouterClient()

        raise ValueError(
            f"Unsupported LLM provider: {LLM_PROVIDER}"
        )