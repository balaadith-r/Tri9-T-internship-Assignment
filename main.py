from parser.extractor import PDFExtractor
from parser.classifier import HeadingClassifier
from parser.tree_builder import TreeBuilder


extractor = PDFExtractor("data/ct200_manual.pdf")

raw_blocks = extractor.extract()

classifier = HeadingClassifier()

parsed = classifier.classify(raw_blocks)

builder = TreeBuilder()

tree = builder.build(parsed)


def print_tree(nodes, indent=0):

    for node in nodes:

        print(
            " " * indent +
            f"{node.section_number} {node.heading}"
            f"({len(node.body)} chars)"
        )

        print_tree(node.children, indent + 4)
    

print_tree(tree.roots)