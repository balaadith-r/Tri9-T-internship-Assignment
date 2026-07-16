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

        document = Document(
            document_name=document_name,
            version=version,
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        flattened = self._flatten_tree(tree)

        inserted_nodes = []

        for parser_node, _ in flattened:

            db_node = Node(
                document_id=document.id,
                parent_id=None,
                logical_hash=parser_node.logical_hash,
                content_hash=parser_node.content_hash,
                section_number=parser_node.section_number,
                heading=parser_node.heading,
                body=parser_node.body,
                page=parser_node.page,
                level=parser_node.level,
            )

            self.db.add(db_node)

            inserted_nodes.append(db_node)

        self.db.commit()

        return document.id   
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