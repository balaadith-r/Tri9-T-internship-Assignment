import os
import sys
from parser.extractor import PDFExtractor
from parser.classifier import HeadingClassifier
from parser.tree_builder import TreeBuilder
from parser.table_extractor import TableExtractor
from parser.table_mapper import TableMapper
from parser.hashing import NodeHasher
from parser.block_filter import BlockFilter

from database.database import SessionLocal
from database.repository import DocumentRepository


if len(sys.argv) != 2:
    print("Usage:")
    print("python ingest_document.py <pdf_path>")
    sys.exit(1)

PDF_PATH = sys.argv[1]

if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    sys.exit(1)


# ----------------------------
# Extract raw text blocks
# ----------------------------

extractor = PDFExtractor(PDF_PATH)
raw_blocks = extractor.extract()


# ----------------------------
# Extract tables
# ----------------------------

table_extractor = TableExtractor(PDF_PATH)
tables = table_extractor.extract()


# ----------------------------
# Remove table text blocks
# ----------------------------

block_filter = BlockFilter()

raw_blocks = block_filter.remove_table_blocks(
    raw_blocks,
    tables,
)


# ----------------------------
# Classify headings
# ----------------------------

classifier = HeadingClassifier()
parsed_blocks = classifier.classify(raw_blocks)


# ----------------------------
# Build document tree
# ----------------------------

builder = TreeBuilder()
tree = builder.build(parsed_blocks)


# ----------------------------
# Attach tables
# ----------------------------

mapper = TableMapper()

tree = mapper.attach_tables(
    tree,
    tables,
)


# ----------------------------
# Compute hashes
# ----------------------------

hasher = NodeHasher()
hasher.hash_tree(tree)


# ----------------------------
# Save document
# ----------------------------

db = SessionLocal()

repository = DocumentRepository(db)

document = repository.save_document(
    tree,
    "CT200",
)

print(f"Successfully ingested CT200 Version {document.version}")

db.close()