from datetime import datetime, UTC
from config import LLM_MODEL
from database.repository import DocumentRepository
from database.qa_store import QAStore
from database.selection_repository import SelectionRepository
from services.prompt_builder import PromptBuilder
from services.llm.factory import LLMFactory


class QAService:

    def __init__(
        self,
        db,
    ):
        self.selection_repository = SelectionRepository(db)
        self.document_repository = DocumentRepository(db)
        self.prompt_builder = PromptBuilder()
        self.llm = LLMFactory.create()
        self.qa_store = QAStore()

    def generate(
        self,
        selection_id: int,
    ) -> str:

        # ----------------------------
        # Load selection
        # ----------------------------

        selection = self.selection_repository.get_selection(
            selection_id
        )

        if selection is None:
            raise ValueError(
                f"Selection {selection_id} not found."
            )

        # ----------------------------
        # Load document
        # ----------------------------

        document = self.document_repository.get_document(
            selection.document_id
        )

        if document is None:
            raise ValueError(
                f"Document {selection.document_id} not found."
            )

        # ----------------------------
        # Load selected nodes
        # ----------------------------

        nodes = self.selection_repository.get_selection_nodes(
            selection_id
        )

        # ----------------------------
        # Build prompt
        # ----------------------------

        prompt = self.prompt_builder.build(nodes)

        # ----------------------------
        # Generate QA
        # ----------------------------

        suite = self.llm.generate(prompt)

        # ----------------------------
        # Wrap metadata
        # ----------------------------

        qa_document = {
            "selection_id": selection.id,
            "document_id": document.id,
            "document_version": document.version,
            "model": LLM_MODEL,
            "generated_at": datetime.now(UTC),
            "stale": False,
            "test_cases": [
                test_case.model_dump()
                for test_case in suite.test_cases
            ],
        }

        # ----------------------------
        # Save
        # ----------------------------

        mongo_id = self.qa_store.save(
            qa_document
        )

        return mongo_id