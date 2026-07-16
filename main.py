from parser.extractor import PDFExtractor
from parser.classifier import HeadingClassifier

extractor = PDFExtractor("data/ct200_manual.pdf")

raw_blocks = extractor.extract()

classifier = HeadingClassifier()

parsed = classifier.classify(raw_blocks)

heading_count = 0

paragraph_count = 0

for block in parsed:

    if block.type == "heading":

        heading_count += 1

        print(
            f"[H] "
            f"{block.section_number:<8}"
            f"{block.heading}"
        )

    else:

        paragraph_count += 1

print()

print(f"Headings   : {heading_count}")
print(f"Paragraphs : {paragraph_count}")