from dataclasses import dataclass, field
from enum import Enum

from database.models import Node


class NodeChangeType(Enum):

    UNCHANGED = "unchanged"
    MODIFIED = "modified"
    ADDED = "added"
    REMOVED = "removed"


@dataclass
class NodeChange:

    change_type: NodeChangeType
    old_node: Node | None = None
    new_node: Node | None = None


@dataclass
class ChangeReport:

    added: list[NodeChange] = field(default_factory=list)
    removed: list[NodeChange] = field(default_factory=list)
    modified: list[NodeChange] = field(default_factory=list)
    unchanged: list[NodeChange] = field(default_factory=list)

    @property
    def total_changes(self) -> int:

        return (
            len(self.added)
            + len(self.removed)
            + len(self.modified)
        )