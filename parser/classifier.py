import re

from parser.models import RawBlock, ParsedBlock


class HeadingClassifier:
    """
    Classifies extracted PDF blocks into headings or paragraphs.
    """

    # Matches:
    # 1. Device Overview
    # 2.1 General Specifications
    # 2.1.1.1 Battery Life
    SECTION_PATTERN = re.compile(
        r"^(\d+(?:\.\d+)*)(?:\.)?\s+(.*)$"
    )

    # Body text in this PDF is ~11pt
    MIN_HEADING_FONT_SIZE = 12

    def classify(self, blocks: list[RawBlock]) -> list[ParsedBlock]:

        parsed_blocks = []

        for block in blocks:

            text = block.text.strip()

            match = self.SECTION_PATTERN.match(text)

            is_heading = (
                match is not None
                and block.is_bold
            )

            if is_heading:

                section = match.group(1)
                heading = match.group(2).strip()

                level = len(section.split("."))

                parsed_blocks.append(
                    ParsedBlock(
                        block=block,
                        type="heading",
                        section_number=section,
                        heading=heading,
                        level=level,
                    )
                )

            else:

                parsed_blocks.append(
                    ParsedBlock(
                        block=block,
                        type="paragraph",
                    )
                )

        return parsed_blocks