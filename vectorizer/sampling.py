"""Helper functions te facilitate sampling from an AST."""

import ast
import samplerjson.jsontree as jsontree

def traverse_nodes(tree):
    """Return a generator that traverses all nodes of a tree."""
    queue = [tree]
    while queue:
        current_node = queue.pop(0)
        children = []
        if isinstance(current_node, ast.AST):
            children = list(ast.iter_child_nodes(current_node))
        else:
            children = list(jsontree.JsonTree.iter_child_nodes(current_node))
        queue.extend(children)
        yield current_node
