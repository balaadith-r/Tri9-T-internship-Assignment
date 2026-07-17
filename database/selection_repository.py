from sqlalchemy.orm import Session
from sqlalchemy.orm import Session, selectinload
from database.models import Node, Selection, SelectionNode


class SelectionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_selection(
        self,
        name: str,
        document_id: int,
        node_ids: list[int],
    ) -> Selection:

        selection = Selection(
            name=name,
            document_id=document_id,
        )

        self.db.add(selection)
        self.db.flush()

        for node_id in node_ids:
            self.db.add(
                SelectionNode(
                    selection_id=selection.id,
                    node_id=node_id,
                )
            )

        self.db.commit()
        self.db.refresh(selection)

        return selection

    def get_selection(
        self,
        selection_id: int,
    ) -> Selection | None:

        return (
            self.db.query(Selection)
            .filter(
                Selection.id == selection_id,
            )
            .first()
        )

    def get_selection_nodes(
        self,
        selection_id: int,
    ) -> list[Node]:

        return (
            self.db.query(Node)
            .options(
                selectinload(Node.tables)
            )
            .join(
                SelectionNode,
                Node.id == SelectionNode.node_id,
            )
            .filter(
                SelectionNode.selection_id == selection_id,
            )
            .order_by(
                Node.page,
                Node.section_number,
            )
            .all()
        )