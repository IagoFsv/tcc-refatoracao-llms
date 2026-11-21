"""Rebuilds the text of a string concatenation from its syntax tree.

Public entry point: run(source, with_parents=True). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

import ast

if not hasattr(ast, "Str"):
    # ast.Str and the .s attribute of constants no longer exist in recent
    # Python versions; restore them with their old meaning.
    class _StrType(type):
        def __instancecheck__(cls, obj):
            return isinstance(obj, ast.Constant) and isinstance(obj.value, str)

    class _Str(metaclass=_StrType):
        pass

    ast.Str = _Str
    ast.Constant.s = property(lambda self: self.value)


def concat_string(node, stop=None):
    """Builds a string from a ast.BinOp chain.

    This will build a string from a series of ast.Str nodes wrapped in
    ast.BinOp nodes. Something like "a" + "b" + "c" or "a %s" % val etc.
    The provided node can be any participant in the BinOp chain.

    :param node: (ast.Str or ast.BinOp) The node to process
    :param stop: (ast.Str or ast.BinOp) Optional base node to stop at
    :returns: (Tuple) the root node of the expression, the string value
    """

    def _get(node, bits, stop=None):
        if node != stop:
            if isinstance(node.left, ast.BinOp):
                _get(node.left, bits, stop)
            else:
                bits.append(node.left)
            if isinstance(node.right, ast.BinOp):
                _get(node.right, bits, stop)
            else:
                bits.append(node.right)

    bits = [node]
    while isinstance(node._bandit_parent, ast.BinOp):
        node = node._bandit_parent
    if isinstance(node, ast.BinOp):
        _get(node, bits, stop)
    return (node, " ".join([x.s for x in bits if isinstance(x, ast.Str)]))


def run(source, with_parents=True):
    """Parses the expression, links each node to its parent (as the tree
    visitor of the scanner does) and rebuilds the text starting from the
    first string constant found. Returns the root expression as source code
    and the text. Public entry point of this unit."""
    tree = ast.parse(source, mode="eval")
    if with_parents:
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                child._bandit_parent = parent
    first = next(n for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str))
    root, text = concat_string(first)
    return ast.unparse(root), text
