from database.database import SessionLocal
from database.repository import DocumentRepository
from services.version_comparator import VersionComparator


def main():

    db = SessionLocal()

    repository = DocumentRepository(db)
    comparator = VersionComparator(db)

    # ----------------------------
    # Show available documents
    # ----------------------------

    documents = repository.list_documents()

    if not documents:
        print("No documents have been ingested.")
        db.close()
        return

    print("\nAvailable Documents\n")

    for document in documents:

        print(
            f"{document.document_name} "
            f"(Version {document.version})"
        )

    # ----------------------------
    # Comparison input
    # ----------------------------

    document_name = input("\nDocument Name: ")

    old_version = int(
        input("Old Version: ")
    )

    new_version = int(
        input("New Version: ")
    )

    report = comparator.compare(
        document_name,
        old_version,
        new_version,
    )

    print("\n----- Comparison Report -----\n")

    print(f"Added      : {len(report.added)}")
    print(f"Removed    : {len(report.removed)}")
    print(f"Modified   : {len(report.modified)}")
    print(f"Unchanged  : {len(report.unchanged)}")

    if report.added:

        print("\nAdded")

        for change in report.added:
            print(
                f"  {change.new_node.section_number} "
                f"{change.new_node.heading}"
            )

    if report.removed:

        print("\nRemoved")

        for change in report.removed:
            print(
                f"  {change.old_node.section_number} "
                f"{change.old_node.heading}"
            )

    if report.modified:

        print("\nModified")

        for change in report.modified:
            print(
                f"  {change.old_node.section_number} "
                f"{change.old_node.heading}"
            )

    db.close()


if __name__ == "__main__":
    main()