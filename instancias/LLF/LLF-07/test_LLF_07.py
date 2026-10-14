"""Testes da instancia LLF-07: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode trocar as lambdas por funcoes
nomeadas, lacos ou compreensoes, e devolver listas em vez de iteradores
(executar converte tudo em listas antes de comparar); o que nao pode mudar e
o conteudo lido e o erro diante de valor gravado que nao e texto.

Os testes fixam o comportamento como ele e: o texto so e separado por virgula
no primeiro nivel, e cada item volta embrulhado em tres listas de um elemento
so (a estrutura gravada nao e recuperada). Espacos sao mantidos e virgula
sobrando gera item vazio.
"""

import pytest

from LLF_07 import executar


def test_tipico_cada_item_volta_em_tres_listas_unitarias():
    assert executar("espada,escudo,pocao") == [
        [[["espada"]]],
        [[["escudo"]]],
        [[["pocao"]]],
    ]


def test_borda_texto_vazio_espacos_e_virgula_sobrando():
    assert executar("") == [[[[""]]]]
    assert executar(" a ,b,") == [[[[" a "]]], [[["b"]]], [[[""]]]]


def test_invalido_valor_gravado_que_nao_e_texto():
    with pytest.raises(AttributeError):
        executar(42)
