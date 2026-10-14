"""Testes da instancia LLF-08: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode trocar as lambdas por funcoes
nomeadas, lacos ou compreensoes, e devolver listas em vez de iteradores
(executar converte tudo em listas antes de comparar); o que nao pode mudar e
o conteudo lido, com o tipo de cada item, e o erro diante de item que nao e
inteiro. A comparacao e pelo repr porque 3 == 3.0 e 1 == True.

Os testes fixam o comportamento como ele e: o texto so e separado por virgula
no primeiro nivel, e cada item volta convertido com int e embrulhado em tres
listas de um elemento so (a estrutura gravada nao e recuperada).
"""

import pytest

from LLF_08 import executar


def test_tipico_cada_inteiro_volta_em_tres_listas_unitarias():
    assert repr(executar("3,-1,+7")) == "[[[[3]]], [[[-1]]], [[[7]]]]"


def test_borda_espacos_zero_e_sublinhado():
    assert repr(executar(" 4 ,0,1_000")) == "[[[[4]]], [[[0]]], [[[1000]]]]"


def test_invalido_item_que_nao_e_inteiro():
    with pytest.raises(ValueError):
        executar("2,3.5")
