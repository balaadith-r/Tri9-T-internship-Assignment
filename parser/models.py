from __future__ import annotations

from typing import List, Optional, Literal, Tuple
from pydantic import BaseModel, Field


# -----------------------------
# Raw PDF Block
# -----------------------------

class RawBlock(BaseModel):

    block_id: int

    page: int

    text: str

    bbox: Tuple[float, float, float, float]

    font_size: float

    font_name: str

    is_bold: bool


# -----------------------------
# Parsed Block
# -----------------------------

class ParsedBlock(BaseModel):

    block: RawBlock

    type: Literal["heading", "paragraph"]

    section_number: Optional[str] = None

    heading: Optional[str] = None

    level: Optional[int] = None


# -----------------------------
# Table
# -----------------------------

class TableBlock(BaseModel):

    page: int

    headers: List[str]

    rows: List[List[str]]


# -----------------------------
# Final Tree Node
# -----------------------------

class Node(BaseModel):

    node_id: str

    parent_id: Optional[str]

    section_number: str

    heading: str

    level: int

    page: int

    body: str = ""

    tables: List[TableBlock] = Field(default_factory=list)

    children: List["Node"] = Field(default_factory=list)

    logical_hash: Optional[str] = None

    content_hash: Optional[str] = None


# -----------------------------
# Entire Document
# -----------------------------

class DocumentTree(BaseModel):

    roots: List[Node] = Field(default_factory=list)