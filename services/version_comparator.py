from sqlalchemy.orm import Session

from database.models import Document, Node
from services.comparison_models import (
    ChangeReport,
    NodeChange,
    NodeChangeType,
)


class VersionComparator:

    def __init__(self, db: Session):
        self.db = db

    def compare(
        self,
        document_name: str,
        old_version: int,
        new_version: int,
    ) -> ChangeReport:

        old_document = (
            self.db.query(Document)
            .filter(
                Document.document_name == document_name,
                Document.version == old_version,
            )
            .first()
        )

        new_document = (
            self.db.query(Document)
            .filter(
                Document.document_name == document_name,
                Document.version == new_version,
            )
            .first()
        )

        if old_document is None:
            raise ValueError(f"Version {old_version} not found.")

        if new_document is None:
            raise ValueError(f"Version {new_version} not found.")

        old_nodes = (
            self.db.query(Node)
            .filter(Node.document_id == old_document.id)
            .all()
        )

        new_nodes = (
            self.db.query(Node)
            .filter(Node.document_id == new_document.id)
            .all()
        )

        return self._compare_nodes(
            old_nodes,
            new_nodes,
        )

    def _compare_nodes(
        self,
        old_nodes: list[Node],
        new_nodes: list[Node],
    ) -> ChangeReport:

        report = ChangeReport()

        old_lookup = {
            node.logical_hash: node
            for node in old_nodes
        }

        matched = set()

        for new_node in new_nodes:

            old_node = old_lookup.get(new_node.logical_hash)

            if old_node is None:

                report.added.append(
                    NodeChange(
                        change_type=NodeChangeType.ADDED,
                        new_node=new_node,
                    )
                )

                continue

            matched.add(old_node.logical_hash)

            if old_node.content_hash == new_node.content_hash:

                report.unchanged.append(
                    NodeChange(
                        change_type=NodeChangeType.UNCHANGED,
                        old_node=old_node,
                        new_node=new_node,
                    )
                )

            else:

                report.modified.append(
                    NodeChange(
                        change_type=NodeChangeType.MODIFIED,
                        old_node=old_node,
                        new_node=new_node,
                    )
                )

        for old_node in old_nodes:

            if old_node.logical_hash not in matched:

                report.removed.append(
                    NodeChange(
                        change_type=NodeChangeType.REMOVED,
                        old_node=old_node,
                    )
                )

        return report