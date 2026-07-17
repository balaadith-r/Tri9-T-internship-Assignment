from parser.table_mapper import TableMapper
from parser.models import DocumentTree, Node, TableBlock


def create_node():

    return Node(
        node_id="1",
        parent_id=None,
        section_number="1",
        heading="Introduction",
        level=1,
        page=1,
        bbox=(0, 100, 200, 120),
    )


def create_table():

    return TableBlock(
        page=1,
        bbox=(0, 150, 200, 250),
        headers=["A", "B"],
        rows=[["1", "2"]],
    )


def test_table_attaches_to_closest_heading():

    mapper = TableMapper()

    node = create_node()

    tree = DocumentTree(roots=[node])

    table = create_table()

    mapper.attach_tables(tree, [table])

    assert len(node.tables) == 1
    assert node.tables[0].headers == ["A", "B"]


def test_table_not_attached_when_no_heading_exists():

    mapper = TableMapper()

    tree = DocumentTree()

    table = create_table()

    mapper.attach_tables(tree, [table])

    assert len(tree.roots) == 0