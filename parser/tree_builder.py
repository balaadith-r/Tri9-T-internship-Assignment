import uuid

from parser.models import ParsedBlock, Node, DocumentTree


class TreeBuilder:
    """
    Builds a hierarchical document tree from classified blocks.
    """

    def build(self, parsed_blocks: list[ParsedBlock]) -> DocumentTree:

        tree = DocumentTree()

        stack: list[Node] = []

        current_node: Node | None = None

        for item in parsed_blocks:

            # -------------------------
            # Paragraph
            # -------------------------

            if item.type == "paragraph":

                if current_node is not None:

                    if current_node.body:
                        current_node.body += "\n\n"

                    current_node.body += item.block.text

                continue

            # -------------------------
            # Heading
            # -------------------------

            node = Node(

                node_id=str(uuid.uuid4()),

                parent_id=None,

                section_number=item.section_number,

                heading=item.heading,

                level=item.level,

                page=item.block.page,
            )

            # Root node

            if not stack:

                tree.roots.append(node)

                stack.append(node)

                current_node = node

                continue

            # Move back until parent found

            while stack and stack[-1].level >= node.level:

                stack.pop()

            if not stack:

                tree.roots.append(node)

            else:

                parent = stack[-1]

                node.parent_id = parent.node_id

                parent.children.append(node)

            stack.append(node)

            current_node = node

        return tree