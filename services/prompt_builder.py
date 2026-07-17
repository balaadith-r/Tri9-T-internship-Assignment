import json
from database.models import Node


class PromptBuilder:
    """Builds the prompt sent to the LLM from selected manual nodes."""

    def build(self, nodes: list[Node]) -> str:
        prompt = self._instructions()

        for node in nodes:
            prompt += self._format_node(node)

        return prompt

    def _instructions(self) -> str:
        return """
You are a Senior QA Engineer responsible for writing verification test cases
for the CardioTrack CT-200, a Class II home blood pressure monitor.

Your task is to analyze the provided sections of the technical manual and
produce high-quality software/device verification test cases.

Generate between 3 and 5 executable test cases.

Each test case MUST verify a specific behaviour explicitly described in
the manual.

A good test case should allow another QA engineer to execute it on the
physical device or firmware without requiring additional interpretation.

Information may appear in normal paragraphs OR tables.

Treat tables and paragraphs as equally authoritative.

Use ONLY information explicitly stated in the provided manual.

DO NOT:

- invent behaviours
- invent thresholds
- invent timings
- invent error codes
- invent specifications
- infer missing values

If the manual does not contain enough information to produce an executable
verification test:

- return an empty "steps" array
- explain what information is missing inside "expected_result"

Return the response using the provided response schema.

Rules:

1. Do NOT output Markdown.
2. Do NOT output explanations.
3. Do NOT wrap the response inside code fences.
4. Every expected_result must be directly supported by the manual.
5. Preserve every numeric value exactly.
6. Preserve every error code exactly.
7. Every source_node_ids entry must correspond to the Node ID shown below.
8. Every source_sections entry must correspond to the displayed section number.
9. Prefer executable verification tests over descriptive summaries.

======================================================================
MANUAL EXCERPTS
======================================================================

"""

    def _format_node(self, node: Node) -> str:
        parts = [
            "=" * 70,
            f"Node ID: {node.id}",
            f"Section: {node.section_number or 'N/A'}",
            f"Heading: {node.heading}",
            "",
            "Body:",
            node.body.strip() if node.body else "",
        ]

        if node.tables:
            parts.append("")
            parts.append("Tables:")

            for index, table in enumerate(node.tables, start=1):
                parts.append("")
                parts.append(f"Table {index}")

                headers = json.loads(table.headers_json) if table.headers_json else []
                rows = json.loads(table.rows_json) if table.rows_json else []

                if headers:
                    parts.append("Headers:")
                    parts.append(" | ".join(str(h) for h in headers))

                if rows:
                    parts.append("Rows:")
                    for row in rows:
                        parts.append(" | ".join(str(cell) for cell in row))

        parts.append("")
        parts.append("=" * 70)
        parts.append("")

        return "\n".join(parts)