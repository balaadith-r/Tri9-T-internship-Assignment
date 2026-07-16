import json

from sqlalchemy.orm import Session

from database.models import Document, Node, Table
from parser.models import DocumentTree


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def save_document(
        self,
        tree: DocumentTree,
        document_name: str,
        version: int,
    ):
        pass
    def _flatten_tree(
        self,
        tree: DocumentTree,
    ) -> list[tuple[ParserNode, ParserNode | None]]:

        flattened = []

        def dfs(node: ParserNode, parent: ParserNode | None):

            flattened.append((node, parent))

            for child in node.children:
                dfs(child, node)

        for root in tree.roots:
            dfs(root, None)

        return flattened