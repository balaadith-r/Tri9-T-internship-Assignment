from parser.hashing import NodeHasher
from parser.models import Node


def create_node():

    return Node(
        node_id="1",
        parent_id=None,
        section_number="1",
        heading="Introduction",
        level=1,
        page=1,
        bbox=(0, 0, 100, 20),
        body="This is the introduction.",
    )


def test_same_node_produces_same_hash():

    hasher = NodeHasher()

    node1 = create_node()
    node2 = create_node()

    hasher.hash_node(node1)
    hasher.hash_node(node2)

    assert node1.logical_hash == node2.logical_hash
    assert node1.content_hash == node2.content_hash


def test_body_change_changes_content_hash():

    hasher = NodeHasher()

    node1 = create_node()
    node2 = create_node()

    node2.body = "Different content"

    hasher.hash_node(node1)
    hasher.hash_node(node2)

    assert node1.content_hash != node2.content_hash


def test_body_change_does_not_change_logical_hash():

    hasher = NodeHasher()

    node1 = create_node()
    node2 = create_node()

    node2.body = "Different body"

    hasher.hash_node(node1)
    hasher.hash_node(node2)

    assert node1.logical_hash == node2.logical_hash