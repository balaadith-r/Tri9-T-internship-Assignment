from database.database import SessionLocal
from database.selection_repository import SelectionRepository
from services.prompt_builder import PromptBuilder


def main():
    # Create database session
    db = SessionLocal()

    try:
        # Load repository
        selection_repo = SelectionRepository(db)

        # Change this to the selection you want to test
        selection_id = 1

        # Fetch nodes belonging to the selection
        nodes = selection_repo.get_selection_nodes(selection_id)

        if not nodes:
            print(f"No nodes found for selection {selection_id}")
            return

        # Build prompt
        prompt_builder = PromptBuilder()
        prompt = prompt_builder.build(nodes)

        print("\n" + "=" * 80)
        print("GENERATED PROMPT")
        print("=" * 80 + "\n")

        print(prompt)

        print("\n" + "=" * 80)
        print("END OF PROMPT")
        print("=" * 80)

    finally:
        db.close()


if __name__ == "__main__":
    main()