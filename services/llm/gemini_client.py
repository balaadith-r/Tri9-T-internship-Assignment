from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL
from schemas.qa_schema import GeneratedTestSuite

from .base import BaseLLMClient


class GeminiClient(BaseLLMClient):
    """Gemini 3.5 Flash implementation."""

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(self, prompt: str) -> GeneratedTestSuite:
        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GeneratedTestSuite,
                temperature=0.2,
            ),
        )

        # The SDK validates against GeneratedTestSuite automatically.
        # Return the validated object.
        return response.parsed