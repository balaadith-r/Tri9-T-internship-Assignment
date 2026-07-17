import json

from openai import (
    OpenAI,
    APIError,
    APIConnectionError,
    RateLimitError,
)
from pydantic import ValidationError

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

        try:

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

            if content is None:
                raise RuntimeError(
                    "LLM returned an empty response."
                )

            data = json.loads(content)

            return GeneratedTestSuite.model_validate(data)

        except json.JSONDecodeError as e:
            raise RuntimeError(
                "LLM returned invalid JSON."
            ) from e

        except ValidationError as e:
            raise RuntimeError(
                "LLM response does not match the expected schema."
            ) from e

        except (
            APIError,
            APIConnectionError,
            RateLimitError,
        ) as e:
            raise RuntimeError(
                "OpenRouter request failed."
            ) from e

        except Exception as e:
            raise RuntimeError(
                "Unexpected error while generating QA."
            ) from e