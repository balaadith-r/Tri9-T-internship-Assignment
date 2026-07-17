from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.repository import DocumentRepository

from services.comparison_models import NodeChangeType
from services.qa_service import QAService
from services.retrieval_service import RetrievalService
from services.selection_service import SelectionService
from services.version_comparator import VersionComparator

app = FastAPI(
    title="Tri9T Assignment",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Request Models
# ----------------------------

class SelectionRequest(BaseModel):
    name: str
    node_ids: list[int]


class QAGenerationRequest(BaseModel):
    selection_id: int


# ----------------------------
# Browse APIs
# ----------------------------

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


# @app.get("/documents/{document_name}/nodes")
# def list_all_nodes(
#     document_name: str,
#     db: Session = Depends(get_db),
# ):
#     repo = DocumentRepository(db)

#     document = repo.get_latest_document(document_name)

#     if document is None:
#         return {"error": "Document not found"}

#     nodes = repo.get_nodes(document.id)

#     return [
#         {
#             "id": node.id,
#             "section_number": node.section_number,
#             "heading": node.heading,
#             "level": node.level,
#         }
#         for node in nodes
#     ]
@app.get("/documents/{document_name}/nodes")
def list_all_nodes(
    document_name: str,
    version: int | None = None,
    db: Session = Depends(get_db),
):
    repo = DocumentRepository(db)

    if version is None:
        document = repo.get_latest_document(document_name)
    else:
        document = repo.get_document_version(
            document_name,
            version,
        )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    nodes = repo.get_nodes(document.id)

    return [
        {
            "id": node.id,
            "section_number": node.section_number,
            "heading": node.heading,
            "level": node.level,
        }
        for node in nodes
    ]


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

    target_node = repo.get_node(node_id)

    if target_node is None:
        return {"error": "Node not found"}

    target_hash = target_node.logical_hash

    comparator = VersionComparator(db)

    report = comparator.compare(
        document_name,
        old_version,
        new_version,
    )

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

                else:
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


# ----------------------------
# Selection API
# ----------------------------

@app.post("/selections")
def create_selection(
    request: SelectionRequest,
    db: Session = Depends(get_db),
):
    service = SelectionService(db)

    try:
        selection = service.create_selection(
            name=request.name,
            node_ids=request.node_ids,
        )

        return {
            "selection_id": selection.id,
            "selection_name": selection.name,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ----------------------------
# LLM Generation API
# ----------------------------

@app.post("/qa/generate")
def generate_qa(
    request: QAGenerationRequest,
    db: Session = Depends(get_db),
):
    service = QAService(db)

    try:
        mongo_id = service.generate(
            request.selection_id
        )

        return {
            "message": "QA generation completed successfully.",
            "mongo_id": str(mongo_id),
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ----------------------------
# Retrieval APIs
# ----------------------------

@app.get("/qa/{selection_id}")
def get_latest_qa(selection_id: int):
    service = RetrievalService()

    result = service.get_latest(selection_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="QA not found.",
        )

    return result


@app.get("/qa/{selection_id}/history")
def get_qa_history(selection_id: int):
    service = RetrievalService()

    return service.get_history(selection_id)


@app.get("/qa/node/{node_id}")
def get_qa_by_node(node_id: int):
    service = RetrievalService()

    result = service.get_by_node_id(node_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="QA not found.",
        )

    return result