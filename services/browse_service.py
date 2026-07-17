from database.document_repository import DocumentRepository
from services.version_comparator import VersionComparator


class BrowseService:

    def __init__(self, db):
        self.repository = DocumentRepository(db)
        self.version_comparator = VersionComparator(db)

    def list_top_level_sections(
        self,
        document_name: str,
    ):
        latest = self.repository.get_latest_document(document_name)

        if latest is None:
            raise ValueError("Document not found.")

        return self.repository.get_root_nodes(latest.id)

    def get_node(
        self,
        node_id: int,
    ):
        node = self.repository.get_node(node_id)

        if node is None:
            raise ValueError("Node not found.")

        return node

    def search(
        self,
        document_name: str,
        query: str,
    ):
        latest = self.repository.get_latest_document(document_name)

        if latest is None:
            raise ValueError("Document not found.")

        return self.repository.search_nodes(
            latest.id,
            query,
        )

    def compare_versions(
        self,
        document_name: str,
        old_version: int,
        new_version: int,
    ):
        return self.version_comparator.compare(
            document_name,
            old_version,
            new_version,
        )