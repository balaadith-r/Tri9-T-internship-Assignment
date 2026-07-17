from database.database import SessionLocal
from database.repository import DocumentRepository
from services.selection_service import SelectionService


def main():

    db = SessionLocal()

    document_repository = DocumentRepository(db)
    selection_service = SelectionService(db)

    # ----------------------------
    # Show available document versions
    # ----------------------------

    documents = document_repository.list_documents()

    if not documents:
        print("No documents have been ingested.")
        return

    print("\nAvailable Documents\n")

    for document in documents:

        print(
            f"{document.id}) "
            f"{document.document_name} "
            f"(Version {document.version})"
        )

    # ----------------------------
    # Choose document version
    # ----------------------------

    document_id = int(
        input("\nSelect Document ID: ")
    )

    nodes = document_repository.get_nodes(document_id)

    if not nodes:
        print("No nodes found.")
        return

    # ----------------------------
    # Show available nodes
    # ----------------------------

    print("\nAvailable Nodes\n")

    for node in nodes:

        print(
            f"{node.id:<4}"
            f"{node.section_number:<8}"
            f"{node.heading}"
        )

    # ----------------------------
    # Selection details
    # ----------------------------

    name = input("\nSelection Name: ")

    node_ids = [

        int(node_id.strip())

        for node_id in input(
            "Node IDs (comma separated): "
        ).split(",")

    ]

    # ----------------------------
    # Create selection
    # ----------------------------

    selection = selection_service.create_selection(
        name=name,
        node_ids=node_ids,
    )

    print("\nSelection Created Successfully\n")

    print(f"Selection ID   : {selection.id}")
    print(f"Selection Name : {selection.name}")

    db.close()


if __name__ == "__main__":
    main()