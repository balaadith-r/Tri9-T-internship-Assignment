from parser.extractor import PDFExtractor
from parser.classifier import HeadingClassifier
from parser.tree_builder import TreeBuilder
from parser.table_extractor import TableExtractor
from parser.table_mapper import TableMapper
from parser.hashing import NodeHasher
from parser.block_filter import BlockFilter

from database.database import SessionLocal
from database.repository import DocumentRepository
from services.version_comparator import VersionComparator


#PDF_PATH = "data/ct200_manual.pdf"
PDF_PATH = "data/ct200_manual_v2.pdf"


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

repo = DocumentRepository(db)

document = repo.save_document(
    tree,
    "CT200",
)

print(
    f"Saved Version {document.version}"
)

if document.version > 1:

    comparator = VersionComparator(db)

    report = comparator.compare(
        "CT200",
        document.version - 1,
        document.version,
    )

    print("\n----- Comparison Report -----")
    print("\n----- Added -----")
    for change in report.added:
        print(change.new_node.section_number, "-", change.new_node.heading)

    print("\n----- Removed -----")
    for change in report.removed:
        print(change.old_node.section_number, "-", change.old_node.heading)

    print("\n----- Modified -----")
    for change in report.modified:
        print(change.old_node.section_number, "-", change.old_node.heading)

    print("\n----- Unchanged -----")
    for change in report.unchanged:
        print(change.old_node.section_number, "-", change.old_node.heading)