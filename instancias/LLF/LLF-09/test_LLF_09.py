"""Testes da instancia LLF-09: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode trocar as lambdas por funcoes
nomeadas, lacos ou compreensoes, e devolver listas em vez de iteradores
(executar converte tudo em listas antes de comparar); o que nao pode mudar e
o conteudo lido, com o tipo de cada item, e o erro diante de item que nao e
numero. A comparacao e pelo repr porque -2 == -2.0.

Os testes fixam o comportamento como ele e: o texto so e separado por virgula
no primeiro nivel, e cada item volta convertido com float e embrulhado em
tres listas de um elemento so (a estrutura gravada nao e recuperada).
"""

import pytest

from LLF_09 import executar


def test_tipico_cada_real_volta_em_tres_listas_unitarias():
    assert repr(executar("1.5,-2,3e2")) == "[[[[1.5]]], [[[-2.0]]], [[[300.0]]]]"


def test_borda_espacos_infinito_e_sublinhado():
    assert repr(executar(" 0.25 ,inf,1_0")) == "[[[[0.25]]], [[[inf]]], [[[10.0]]]]"


def test_invalido_item_que_nao_e_numero():
    with pytest.raises(ValueError):
        executar("1.5,abc")
