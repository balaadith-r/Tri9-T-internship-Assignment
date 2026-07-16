from parser.models import RawBlock, TableBlock


class BlockFilter:
    """
    Removes text blocks that belong to extracted tables.
    """

    def remove_table_blocks(
        self,
        blocks: list[RawBlock],
        tables: list[TableBlock],
    ) -> list[RawBlock]:

        filtered = []

        for block in blocks:

            keep = True

            # Block center
            center_x = (block.bbox[0] + block.bbox[2]) / 2
            center_y = (block.bbox[1] + block.bbox[3]) / 2

            for table in tables:

                if block.page != table.page:
                    continue

                x0, y0, x1, y1 = table.bbox

                if (
                    x0 <= center_x <= x1
                    and
                    y0 <= center_y <= y1
                ):
                    keep = False
                    break

            if keep:
                filtered.append(block)

        return filtered