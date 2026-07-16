from parser.models import DocumentTree, TableBlock


class TableMapper:

    def attach_tables(
        self,
        tree: DocumentTree,
        tables: list[TableBlock],
    ) -> DocumentTree:

        all_nodes = []

        def collect(nodes):
            for node in nodes:
                all_nodes.append(node)
                collect(node.children)

        collect(tree.roots)

        for table in tables:

            table_top = table.bbox[1]

            candidates = [
                node
                for node in all_nodes
                if (
                    node.page == table.page
                    and node.bbox[1] < table_top
                )
            ]

            if not candidates:
                continue

            target = max(
                candidates,
                key=lambda n: n.bbox[1]
            )

            target.tables.append(table)

        return tree