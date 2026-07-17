import argparse

from database.database import SessionLocal
from services.qa_service import QAService


def main():

    parser = argparse.ArgumentParser(
        description="Generate QA test cases for a selection."
    )

    parser.add_argument(
        "selection_id",
        type=int,
        help="Selection ID",
    )

    args = parser.parse_args()

    db = SessionLocal()

    try:
        qa_service = QAService(db)

        mongo_id = qa_service.generate(
            args.selection_id
        )

        print("\nQA generation completed successfully.")
        print(f"MongoDB ID: {mongo_id}")

    finally:
        db.close()


if __name__ == "__main__":
    main()