from abc import ABC, abstractmethod

from schemas.qa_schema import GeneratedTestSuite


class BaseLLMClient(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    def generate_test_suite(self, prompt: str) -> GeneratedTestSuite:
        """Generate a structured QA test suite from the supplied prompt."""
        pass