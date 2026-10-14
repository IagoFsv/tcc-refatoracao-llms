"""Testes da instancia LLF-10: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode trocar as lambdas por funcoes
nomeadas, lacos ou compreensoes, e devolver listas em vez de iteradores
(executar converte tudo em listas antes de comparar); o que nao pode mudar e
o conteudo lido, com o tipo de cada item, e o erro diante de valor gravado
que nao e texto. A comparacao e pelo repr porque 1 == True.

Os testes fixam o comportamento como ele e, inclusive o defeito do original:
cada item passa por bool, entao qualquer texto nao vazio vira True, ate
"False" e "0"; so o item vazio vira False. O texto so e separado por virgula
no primeiro nivel, e cada item volta embrulhado em tres listas de um elemento
so (a estrutura gravada nao e recuperada).
"""

import pytest

from LLF_10 import executar


def test_tipico_todo_texto_nao_vazio_vira_true():
    assert repr(executar("True,False,0")) == "[[[[True]]], [[[True]]], [[[True]]]]"


def test_borda_texto_vazio_e_virgulas_sobrando_viram_false():
    assert repr(executar("")) == "[[[[False]]]]"
    assert repr(executar("a,,")) == "[[[[True]]], [[[False]]], [[[False]]]]"


def test_invalido_valor_gravado_que_nao_e_texto():
    with pytest.raises(AttributeError):
        executar(42)
