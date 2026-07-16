import fitz

from parser.models import RawBlock


class PDFExtractor:
    """
    Extract raw text blocks from the PDF.

    This class is ONLY responsible for extraction.

    It knows nothing about headings,
    tables, hierarchy or versions.
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract(self) -> list[RawBlock]:

        doc = fitz.open(self.pdf_path)

        blocks = []

        block_id = 0

        for page_number, page in enumerate(doc, start=1):

            page_dict = page.get_text("dict")

            for block in page_dict["blocks"]:

                if block["type"] != 0:
                    continue

                text = []
                font_sizes = []
                fonts = []

                bold = False

                for line in block["lines"]:

                    for span in line["spans"]:

                        value = span["text"].strip()

                        if not value:
                            continue

                        text.append(value)

                        font_sizes.append(span["size"])

                        fonts.append(span["font"])

                        if "bold" in span["font"].lower():

                            bold = True

                if not text:
                    continue

                blocks.append(
                    RawBlock(
                        block_id=block_id,
                        page=page_number,
                        text=" ".join(text),
                        bbox=tuple(block["bbox"]),
                        font_size=max(font_sizes),
                        font_name=fonts[0],
                        is_bold=bold,
                    )
                )

                block_id += 1

        doc.close()

        return blocks