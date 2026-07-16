from datetime import datetime

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