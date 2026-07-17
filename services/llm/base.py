from abc import ABC, abstractmethod

from schemas.qa_schema import GeneratedTestSuite


class BaseLLMClient(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> GeneratedTestSuite:
        pass