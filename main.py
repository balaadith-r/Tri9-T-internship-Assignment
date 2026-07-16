from parser.extractor import PDFExtractor
from parser.classifier import HeadingClassifier
from parser.tree_builder import TreeBuilder
from parser.table_extractor import TableExtractor
from parser.table_mapper import TableMapper
from parser.hashing import NodeHasher

PDF_PATH = "data/ct200_manual.pdf"

# ----------------------------
# Extract raw text blocks
# ----------------------------
extractor = PDFExtractor(PDF_PATH)
raw_blocks = extractor.extract()

# ----------------------------
# Classify headings & paragraphs
# ----------------------------
classifier = HeadingClassifier()
parsed_blocks = classifier.classify(raw_blocks)

# ----------------------------
# Build document tree
# ----------------------------
builder = TreeBuilder()
tree = builder.build(parsed_blocks)

# ----------------------------
# Extract tables
# ----------------------------
table_extractor = TableExtractor(PDF_PATH)
tables = table_extractor.extract()

# ----------------------------
# Attach tables to nodes
# ----------------------------
mapper = TableMapper()
tree = mapper.attach_tables(tree, tables)

# ----------------------------
# Compute hashes
# ----------------------------
hasher = NodeHasher()
hasher.hash_tree(tree)


# ----------------------------
# Debug Print
# ----------------------------
def print_tree(nodes, indent=0):
    for node in nodes:

        print(" " * indent + f"{node.section_number} {node.heading}")

        print(
            " " * (indent + 4) +
            f"Logical Hash : {node.logical_hash[:10]}..."
        )

        print(
            " " * (indent + 4) +
            f"Content Hash : {node.content_hash[:10]}..."
        )

        if node.tables:
            for table in node.tables:
                print(
                    " " * (indent + 4) +
                    f"Headers: {table.headers}"
                )
                print(
                    " " * (indent + 4) +
                    f"Rows: {len(table.rows)}"
                )

        print_tree(node.children, indent + 4)


print_tree(tree.roots)