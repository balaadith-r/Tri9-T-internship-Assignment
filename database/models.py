from datetime import datetime
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)

from database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    document_name = Column(Text, nullable=False)

    version = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
    )

    parent_id = Column(
        Integer,
        ForeignKey("nodes.id"),
        nullable=True,
    )

    logical_hash = Column(Text, nullable=False)

    content_hash = Column(Text, nullable=False)

    section_number = Column(Text)

    heading = Column(Text, nullable=False)

    body = Column(Text)

    page = Column(Integer)

    level = Column(Integer)

    tables = relationship(
        "Table",
        back_populates="node",
        cascade="all, delete-orphan",
    )


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)

    node_id = Column(
        Integer,
        ForeignKey("nodes.id"),
        nullable=False,
    )

    headers_json = Column(Text)

    rows_json = Column(Text)

    node = relationship(
        "Node",
        back_populates="tables",
    )


class Selection(Base):
    __tablename__ = "selections"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(Text, nullable=False)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class SelectionNode(Base):
    __tablename__ = "selection_nodes"

    selection_id = Column(
        Integer,
        ForeignKey("selections.id"),
        primary_key=True,
    )

    node_id = Column(
        Integer,
        ForeignKey("nodes.id"),
        primary_key=True,
    )