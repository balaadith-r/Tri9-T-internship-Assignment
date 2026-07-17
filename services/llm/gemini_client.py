from google import genai
from google.genai import types
from pydantic import ValidationError

from config import GEMINI_API_KEY, GEMINI_MODEL
from schemas.qa_schema import GeneratedTestSuite

from .base import BaseLLMClient


class GeminiClient(BaseLLMClient):
    """Gemini 3.5 Flash implementation."""

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(
        self,
        prompt: str,
    ) -> GeneratedTestSuite:

        try:

            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=GeneratedTestSuite,
                    temperature=0.2,
                ),
            )

            if response.parsed is None:
                raise RuntimeError(
                    "LLM returned an empty response."
                )

            return response.parsed

        except ValidationError as e:
            raise RuntimeError(
                "LLM response does not match the expected schema."
            ) from e

        except Exception as e:
            raise RuntimeError(
                "Unexpected error while generating QA."
            ) from e