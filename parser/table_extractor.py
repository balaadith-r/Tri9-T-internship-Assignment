import pdfplumber

from parser.models import TableBlock


class TableExtractor:
    """
    Extracts the primary structured table from each page.

    The CT-200 manuals contain one meaningful table per page.
    pdfplumber returns several fragmented tables, so we keep
    the largest valid one.
    """

    def __init__(self, pdf_path: str):

        self.pdf_path = pdf_path

    def extract(self) -> list[TableBlock]:

        extracted = []

        with pdfplumber.open(self.pdf_path) as pdf:

            for page_number, page in enumerate(pdf.pages, start=1):

                found_tables = page.find_tables()

                if not found_tables:
                    continue

                # Keep the largest detected table
                table = max(
                    found_tables,
                    key=lambda t: len(t.extract())
                )

                data = table.extract()

                if len(data) < 2:
                    continue

                extracted.append(
                    TableBlock(
                        page=page_number,
                        bbox=table.bbox,
                        headers=data[0],
                        rows=data[1:],
                    )
                )

        return extracted