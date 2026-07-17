from sqlalchemy.orm import Session

from database.models import Node, Selection
from database.selection_repository import SelectionRepository


class SelectionService:

    def __init__(self, db: Session):

        self.db = db
        self.repository = SelectionRepository(db)

    def create_selection(
        self,
        name: str,
        node_ids: list[int],
    ) -> Selection:

        if not node_ids:
            raise ValueError("Selection cannot be empty.")

        nodes = (
            self.db.query(Node)
            .filter(Node.id.in_(node_ids))
            .all()
        )

        if len(nodes) != len(node_ids):
            raise ValueError("One or more node IDs do not exist.")

        document_ids = {
            node.document_id
            for node in nodes
        }

        if len(document_ids) != 1:
            raise ValueError(
                "Selection must contain nodes from a single document version."
            )

        document_id = document_ids.pop()

        return self.repository.create_selection(
            name=name,
            document_id=document_id,
            node_ids=node_ids,
        )