from parser.tree_builder import TreeBuilder
from parser.models import RawBlock, ParsedBlock


def test_single_root_node():

    builder = TreeBuilder()

    blocks = [
        ParsedBlock(
            block=RawBlock(
                block_id=1,
                page=1,
                text="1 Introduction",
                bbox=(0, 0, 100, 20),
                font_size=14,
                font_name="Arial-Bold",
                is_bold=True,
            ),
            type="heading",
            section_number="1",
            heading="Introduction",
            level=1,
        )
    ]

    tree = builder.build(blocks)

    assert len(tree.roots) == 1
    assert tree.roots[0].heading == "Introduction"
    assert tree.roots[0].parent_id is None


def test_parent_child_relationship():

    builder = TreeBuilder()

    blocks = [
        ParsedBlock(
            block=RawBlock(
                block_id=1,
                page=1,
                text="1 Introduction",
                bbox=(0, 0, 0, 0),
                font_size=14,
                font_name="Arial-Bold",
                is_bold=True,
            ),
            type="heading",
            section_number="1",
            heading="Introduction",
            level=1,
        ),
        ParsedBlock(
            block=RawBlock(
                block_id=2,
                page=1,
                text="1.1 Scope",
                bbox=(0, 0, 0, 0),
                font_size=14,
                font_name="Arial-Bold",
                is_bold=True,
            ),
            type="heading",
            section_number="1.1",
            heading="Scope",
            level=2,
        ),
    ]

    tree = builder.build(blocks)

    root = tree.roots[0]

    assert len(root.children) == 1
    assert root.children[0].heading == "Scope"
    assert root.children[0].parent_id == root.node_id


def test_paragraph_added_to_current_section():

    builder = TreeBuilder()

    blocks = [
        ParsedBlock(
            block=RawBlock(
                block_id=1,
                page=1,
                text="1 Introduction",
                bbox=(0, 0, 0, 0),
                font_size=14,
                font_name="Arial-Bold",
                is_bold=True,
            ),
            type="heading",
            section_number="1",
            heading="Introduction",
            level=1,
        ),
        ParsedBlock(
            block=RawBlock(
                block_id=2,
                page=1,
                text="This is the introduction.",
                bbox=(0, 0, 0, 0),
                font_size=11,
                font_name="Arial",
                is_bold=False,
            ),
            type="paragraph",
        ),
    ]

    tree = builder.build(blocks)

    assert tree.roots[0].body == "This is the introduction."