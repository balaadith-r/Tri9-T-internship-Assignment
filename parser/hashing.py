import hashlib
import json

from parser.models import DocumentTree, Node


class NodeHasher:
    """
    Computes logical and content hashes for every node in the document tree.
    """

    @staticmethod
    def _sha256(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def hash_node(self, node: Node) -> None:

        # ---------- Logical Hash ----------
        logical_text = f"{node.section_number}|{node.heading}"

        node.logical_hash = self._sha256(logical_text)

        # ---------- Content Hash ----------

        table_data = []

        for table in node.tables:
            table_data.append({
                "headers": table.headers,
                "rows": table.rows,
            })

        content = {
            "heading": node.heading,
            "body": node.body,
            "tables": table_data,
        }

        content_text = json.dumps(
            content,
            sort_keys=True,
            ensure_ascii=False,
        )

        node.content_hash = self._sha256(content_text)

    def hash_tree(self, tree: DocumentTree) -> None:

        def dfs(node: Node):

            self.hash_node(node)

            for child in node.children:
                dfs(child)

        for root in tree.roots:
            dfs(root)