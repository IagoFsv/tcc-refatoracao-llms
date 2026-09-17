"""Camada de compatibilidade do porte do Pysmell para Python 3.

O Pysmell original (Chen et al.) e codigo Python 2 e depende de duas coisas
que mudaram no Python 3:

1. `astunparse`, que le a AST de volta para texto. A biblioteca ainda existe
   para Python 3, mas acessa `Constant.n` e `Constant.s`, removidos no
   Python 3.12+. O shim abaixo devolve esses atributos.

   NAO troque `astunparse.unparse` por `ast.unparse`: o `astunparse` envolve
   cada lambda e cada expressao ternaria em parenteses, e o `ast.unparse` nao.
   Isso muda a metrica NOC (comprimento da expressao) e faz o detector perder
   instancias de Long Lambda Function que o Zhang et al. (2024) reportam.

2. Tipos da AST que sumiram no Python 3 (AugLoad, AugStore, Param, Index,
   ExtSlice, ...). Eles aparecem nas listas de filtro do contador de operandos
   (metrica NOO) do `astChecker.py`. `tipos_ignorados()` monta a mesma lista,
   pulando os que nao existem mais na versao em uso.
"""

import ast

if not hasattr(ast.Constant, "n"):
    ast.Constant.n = property(lambda self: self.value)
    ast.Constant.s = property(lambda self: self.value)

import astunparse  # noqa: E402  (precisa vir depois do shim acima)

unparse = astunparse.unparse

# Mesma lista do astChecker.py original, em ordem.
_NOMES_IGNORADOS = (
    "Load", "Store", "Del", "AugLoad", "AugStore", "Param",
    "Ellipsis", "ExtSlice", "Index", "And", "Or",
    "Add", "Sub", "Mult", "Div", "Mod", "Pow", "LShift",
    "RShift", "BitOr", "BitXor", "BitAnd", "FloorDiv",
    "Invert", "Not", "UAdd", "USub",
    "Eq", "NotEq", "Lt", "LtE", "Gt", "GtE", "Is", "IsNot", "In", "NotIn",
    "comprehension", "ExceptHandler", "arguments", "keyword", "alias",
)


def tipos_ignorados():
    """Tipos da AST que nao contam como operando na metrica NOO."""
    return [t for t in (getattr(ast, nome, None) for nome in _NOMES_IGNORADOS) if t is not None]
