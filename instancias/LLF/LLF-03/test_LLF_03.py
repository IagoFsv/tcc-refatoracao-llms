"""Testes da instancia LLF-03: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode trocar as lambdas por funcoes
nomeadas, lacos ou compreensoes; o que nao pode mudar e o texto gravado na
configuracao, a mensagem registrada no log depois da gravacao e o erro diante
de item que nao e texto.

Os testes fixam o comportamento como ele e: os quatro niveis viram uma lista
plana separada por virgula (a estrutura se perde), nivel vazio deixa virgula
sobrando e texto no ultimo nivel e separado letra por letra.
"""

import logging

import pytest

from LLF_03 import executar


def test_tipico_quatro_niveis_viram_texto_separado_por_virgula(caplog):
    caplog.set_level(logging.INFO)
    valor = [
        [[["a", "b"], ["c"]], [["d"]]],
        [[["e", "f"]]],
    ]

    assert executar(valor) == "a,b,c,d,e,f"
    assert caplog.messages == ["Config: {'mundo': {'regioes': 'a,b,c,d,e,f'}}"]


def test_borda_texto_no_ultimo_nivel_niveis_vazios_e_tuplas(caplog):
    caplog.set_level(logging.INFO)

    assert executar([[["xy", ""]], [[]], []]) == "x,y,,,"  # "xy" sai letra por letra
    assert executar([]) == ""
    assert executar((((("pa",),),),)) == "pa"
    assert caplog.messages[0] == "Config: {'mundo': {'regioes': 'x,y,,,'}}"


def test_invalido_item_que_nao_e_texto():
    with pytest.raises(TypeError):
        executar([[[[1, 2]]]])
