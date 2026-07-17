import argparse

from database.database import SessionLocal
from services.staleness_service import StalenessService


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "selection_id",
        type=int,
    )

    args = parser.parse_args()

    db = SessionLocal()

    try:

        service = StalenessService(db)

        stale = service.check(
            args.selection_id,
        )

        if stale:
            print("QA marked as stale.")

        else:
            print("QA is up to date.")

    finally:
        db.close()


if __name__ == "__main__":
    main()