from pydantic import BaseModel, Field

class TestCase(BaseModel):
    title: str = Field(
        description="Short descriptive title of the QA test."
    )

    preconditions: str = Field(
        description="Required state before executing the test."
    )

    steps: list[str] = Field(
        description="Ordered execution steps."
    )

    expected_result: str = Field(
        description="Expected observable behaviour."
    )

    source_sections: list[str] = Field(
        description="Manual section numbers used."
    )

    source_node_ids: list[int] = Field(
        description="Database node IDs used to create this test."
    )

class GeneratedTestSuite(BaseModel):
    test_cases: list[TestCase]