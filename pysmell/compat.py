"""Compatibility layer of the Pysmell port to Python 3.

The original Pysmell (Chen et al.) is Python 2 code and depends on two
things that changed in Python 3:

1. `astunparse`, which turns the AST back into text. The library still exists
   for Python 3, but it reads `Constant.n` and `Constant.s`, removed in
   Python 3.12+. The shim below brings those attributes back.

   DO NOT replace `astunparse.unparse` with `ast.unparse`: `astunparse` wraps
   every lambda and every ternary expression in parentheses, and
   `ast.unparse` does not. That changes the NOC metric (expression length)
   and makes the detector miss Long Lambda Function instances that Zhang et
   al. (2024) report.

2. AST types removed in Python 3 (AugLoad, AugStore, Param, Index, ExtSlice,
   ...). They appear in the filter lists of the operand counter (NOO metric)
   in `astChecker.py`. `ignored_types()` builds the same list, skipping the
   ones that no longer exist in the running version.
"""

import ast

if not hasattr(ast.Constant, "n"):
    ast.Constant.n = property(lambda self: self.value)
    ast.Constant.s = property(lambda self: self.value)

import astunparse  # noqa: E402  (must come after the shim above)

unparse = astunparse.unparse

# Same list as in the original astChecker.py, in order.
_IGNORED_NAMES = (
    "Load", "Store", "Del", "AugLoad", "AugStore", "Param",
    "Ellipsis", "ExtSlice", "Index", "And", "Or",
    "Add", "Sub", "Mult", "Div", "Mod", "Pow", "LShift",
    "RShift", "BitOr", "BitXor", "BitAnd", "FloorDiv",
    "Invert", "Not", "UAdd", "USub",
    "Eq", "NotEq", "Lt", "LtE", "Gt", "GtE", "Is", "IsNot", "In", "NotIn",
    "comprehension", "ExceptHandler", "arguments", "keyword", "alias",
)


def ignored_types():
    """AST types that do not count as operands in the NOO metric."""
    return [t for t in (getattr(ast, name, None) for name in _IGNORED_NAMES) if t is not None]
