from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.repository import DocumentRepository
from services.version_comparator import VersionComparator
from services.comparison_models import NodeChangeType

app = FastAPI(
    title="Tri9T Assignment",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/documents/{document_name}/sections")
def list_sections(
    document_name: str,
    db: Session = Depends(get_db),
):
    repo = DocumentRepository(db)

    document = repo.get_latest_document(document_name)

    if document is None:
        return {"error": "Document not found"}

    return repo.get_root_nodes(document.id)

@app.get("/nodes/{node_id}")
def get_node(
    node_id: int,
    db: Session = Depends(get_db),
):
    repo = DocumentRepository(db)

    node = repo.get_node(node_id)

    if node is None:
        return {"error": "Node not found"}

    return node

@app.get("/documents/{document_name}/search")
def search_nodes(
    document_name: str,
    query: str,
    db: Session = Depends(get_db),
):
    repo = DocumentRepository(db)

    document = repo.get_latest_document(document_name)

    if document is None:
        return {"error": "Document not found"}

    return repo.search_nodes(
        document.id,
        query,
    )

@app.get("/documents/{document_name}/diff")
def node_diff(
    document_name: str,
    old_version: int,
    new_version: int,
    node_id: int,
    db: Session = Depends(get_db),
):
    repo = DocumentRepository(db)

    # Step 1: Find the requested node
    target_node = repo.get_node(node_id)

    if target_node is None:
        return {"error": "Node not found"}

    target_hash = target_node.logical_hash

    # Step 2: Compare the two document versions
    comparator = VersionComparator(db)
    report = comparator.compare(
        document_name,
        old_version,
        new_version,
    )

    # Step 3: Search the comparison result using logical_hash
    for change_list in (
        report.modified,
        report.unchanged,
        report.added,
        report.removed,
    ):
        for change in change_list:

            node = change.new_node or change.old_node

            if node.logical_hash == target_hash:
                if change.change_type == NodeChangeType.UNCHANGED:
                    summary = "No changes detected."
                elif change.change_type == NodeChangeType.MODIFIED:
                    summary = (
                        f"Node content changed between version "
                        f"{old_version} and version {new_version}."
                    )
                elif change.change_type == NodeChangeType.ADDED:
                    summary = (
                        f"Node was added in version {new_version}."
                    )
                else:  # REMOVED
                    summary = (
                        f"Node was removed after version {old_version}."
                    )

                return {
                    "changed": change.change_type != NodeChangeType.UNCHANGED,
                    "change_type": change.change_type.value,
                    "heading": node.heading,
                    "section_number": node.section_number,
                    "summary": summary,
                }

    return {"error": "Node not found in comparison"}