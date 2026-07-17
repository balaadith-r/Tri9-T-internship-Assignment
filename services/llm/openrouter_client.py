import json

from openai import OpenAI

from config import OPENROUTER_API_KEY, OPENROUTER_MODEL
from schemas.qa_schema import GeneratedTestSuite

from .base import BaseLLMClient


class OpenRouterClient(BaseLLMClient):
    """OpenRouter implementation."""

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

    def generate(
        self,
        prompt: str,
    ) -> GeneratedTestSuite:

        response = self.client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        data = json.loads(content)

        return GeneratedTestSuite.model_validate(data)