from parser.extractor import PDFExtractor
from parser.classifier import HeadingClassifier
from parser.tree_builder import TreeBuilder
from parser.table_extractor import TableExtractor
from parser.table_mapper import TableMapper


PDF_PATH = "data/ct200_manual.pdf"

# Extract text
extractor = PDFExtractor(PDF_PATH)
raw_blocks = extractor.extract()

# Classify headings
classifier = HeadingClassifier()
parsed_blocks = classifier.classify(raw_blocks)

# Build tree
builder = TreeBuilder()
tree = builder.build(parsed_blocks)

# Extract tables
table_extractor = TableExtractor(PDF_PATH)
tables = table_extractor.extract()

# Attach tables
mapper = TableMapper()
tree = mapper.attach_tables(tree, tables)

# def print_tree(nodes, indent=0):
#     for node in nodes:

#         print(
#             " " * indent +
#             f"{node.section_number} {node.heading}"
#         )

#         if node.tables:
#             print(
#                 " " * (indent + 4) +
#                 f"Tables: {len(node.tables)}"
#             )

#         print_tree(node.children, indent + 4)

def print_tree(nodes, indent=0):
    for node in nodes:

        print(" " * indent + f"{node.section_number} {node.heading}")

        if node.tables:
            for table in node.tables:
                print(" " * (indent + 4) + f"Headers: {table.headers}")
                print(" " * (indent + 4) + f"Rows: {len(table.rows)}")

        print_tree(node.children, indent + 4)

print_tree(tree.roots)