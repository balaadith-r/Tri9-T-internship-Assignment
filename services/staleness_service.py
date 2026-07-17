from database.repository import DocumentRepository
from database.selection_repository import SelectionRepository
from database.qa_store import QAStore
from services.version_comparator import VersionComparator


class StalenessService:

    def __init__(self, db):
        self.db = db

        self.selection_repo = SelectionRepository(db)
        self.document_repo = DocumentRepository(db)
        self.qa_store = QAStore()
        self.version_comparator = VersionComparator(db)

    def check(
        self,
        selection_id: int,
    ) -> bool:

        qa = self.qa_store.get_latest(selection_id)

        if qa is None:
            raise ValueError("No generated QA found.")

        if qa["stale"]:
            return True

        if self.selection_repo.get_selection(selection_id) is None:
            raise ValueError("Selection not found.")

        document = self.document_repo.get_document(
            qa["document_id"]
        )

        if document is None:
            raise ValueError("Document not found.")

        latest_document = self.document_repo.get_latest_document(
            document.document_name
        )

        if latest_document is None:
            raise ValueError("Latest document not found.")

        if latest_document.version == document.version:
            return False

        report = self.version_comparator.compare(
            document.document_name,
            document.version,
            latest_document.version,
        )

        modified_node_ids = {
            change.old_node.id
            for change in report.modified
            if change.old_node is not None
        }

        for test_case in qa["test_cases"]:

            source_node_ids = set(
                test_case["source_node_ids"]
            )

            if modified_node_ids.intersection(source_node_ids):

                self.qa_store.mark_stale_by_id(
                    str(qa["_id"])
                )

                return True

        return False