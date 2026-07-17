import json

from sqlalchemy.orm import Session
from sqlalchemy import or_
from database.models import Document, Node, Table
from parser.models import DocumentTree, Node as ParserNode


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_latest_document(
        self,
        document_name: str,
    ) -> Document | None:

        return (
            self.db.query(Document)
            .filter(
                Document.document_name == document_name,
            )
            .order_by(Document.version.desc())
            .first()
        )
    
    def get_latest_version(
        self,
        document_name: str,
    ) -> int:

        latest = self.get_latest_document(document_name)

        if latest is None:
            return 0

        return latest.version

    def save_document(
        self,
        tree: DocumentTree,
        document_name: str,
    ) -> Document:

        version = self.get_latest_version(document_name) + 1

        # ----------------------------
        # Save document
        # ----------------------------

        document = Document(
            document_name=document_name,
            version=version,
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        # ----------------------------
        # Flatten tree
        # ----------------------------

        flattened = self._flatten_tree(tree)

        parser_to_db = {}

        # ----------------------------
        # Save nodes
        # ----------------------------

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
            self.db.flush()

            parser_to_db[parser_node.node_id] = db_node

        # ----------------------------
        # Resolve parent relationships
        # ----------------------------

        for parser_node, parser_parent in flattened:

            if parser_parent is None:
                continue

            db_node = parser_to_db[parser_node.node_id]
            db_parent = parser_to_db[parser_parent.node_id]

            db_node.parent_id = db_parent.id

        # ----------------------------
        # Save tables
        # ----------------------------

        for parser_node, _ in flattened:

            db_node = parser_to_db[parser_node.node_id]

            for table in parser_node.tables:

                db_table = Table(
                    node_id=db_node.id,
                    headers_json=json.dumps(table.headers),
                    rows_json=json.dumps(table.rows),
                )

                self.db.add(db_table)

        self.db.commit()

        return document
    
    def list_documents(self) -> list[Document]:

        return (
            self.db.query(Document)
            .order_by(
                Document.document_name,
                Document.version,
            )
            .all()
        )
    def _flatten_tree(
        self,
        tree: DocumentTree,
    ) -> list[tuple[ParserNode, ParserNode | None]]:

        flattened = []

        def dfs(
            node: ParserNode,
            parent: ParserNode | None,
        ):

            flattened.append((node, parent))

            for child in node.children:
                dfs(child, node)

        for root in tree.roots:
            dfs(root, None)

        return flattened
    
    def get_nodes(
        self,
        document_id: int,
    ) -> list[Node]:

        return (
            self.db.query(Node)
            .filter(
                Node.document_id == document_id,
            )
            .order_by(
                Node.page,
                Node.section_number,
            )
            .all()
        )
    
    def get_document(
        self,
        document_id: int,
    ) -> Document | None:

        return (
            self.db.query(Document)
            .filter(
                Document.id == document_id,
            )
            .first()
        )
    def get_node(self, node_id: int) -> Node | None:
        return (
            self.db.query(Node)
            .filter(Node.id == node_id)
            .first()
        )


    def get_root_nodes(self, document_id: int) -> list[Node]:
        return (
            self.db.query(Node)
            .filter(
                Node.document_id == document_id,
                Node.parent_id.is_(None),
            )
            .order_by(Node.section_number)
            .all()
        )


    def get_children(self, parent_id: int) -> list[Node]:
        return (
            self.db.query(Node)
            .filter(Node.parent_id == parent_id)
            .order_by(Node.section_number)
            .all()
        )


    from sqlalchemy import or_

    def search_nodes(
        self,
        document_id: int,
        query: str,
    ) -> list[Node]:

        return (
            self.db.query(Node)
            .filter(
                Node.document_id == document_id,
                or_(
                    Node.heading.ilike(f"%{query}%"),
                    Node.body.ilike(f"%{query}%"),
                ),
            )
            .all()
        )