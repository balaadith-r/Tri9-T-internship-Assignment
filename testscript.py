from database.database import SessionLocal
from database.selection_repository import SelectionRepository

from services.prompt_builder import PromptBuilder
from services.llm.gemini_client import GeminiClient


def main():
    db = SessionLocal()

    try:
        selection_repo = SelectionRepository(db)

        # Change if your selection has a different ID
        selection_id = 1

        nodes = selection_repo.get_selection_nodes(selection_id)

        if not nodes:
            print(f"No nodes found for selection {selection_id}")
            return

        prompt = PromptBuilder().build(nodes)

        print("\nGenerating QA test suite...\n")

        llm = GeminiClient()

        suite = llm.generate_test_suite(prompt)

        print(suite.model_dump_json(indent=2))

    finally:
        db.close()


if __name__ == "__main__":
    main()
