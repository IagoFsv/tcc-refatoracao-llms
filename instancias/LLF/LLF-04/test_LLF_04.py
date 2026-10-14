"""Testes da instancia LLF-04: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode trocar as lambdas por funcoes
nomeadas, lacos ou compreensoes; o que nao pode mudar e o texto gravado na
configuracao, a mensagem registrada no log depois da gravacao e o erro diante
de um ultimo nivel que nao e sequencia.

Os testes fixam o comportamento como ele e: os quatro niveis viram uma lista
plana separada por virgula (a estrutura se perde), qualquer item do ultimo
nivel e convertido com str (inteiro, real, bool, None), nivel vazio deixa
virgula sobrando e texto no ultimo nivel e separado letra por letra.
"""

import logging

import pytest

from LLF_04 import executar


def test_tipico_numeros_em_quatro_niveis_viram_texto(caplog):
    caplog.set_level(logging.INFO)
    valor = [
        [[[1, 2.5], [3]], [[-4]]],
        [[[0.1, 6]]],
    ]

    assert executar(valor) == "1,2.5,3,-4,0.1,6"
    assert caplog.messages == ["Config: {'mundo': {'regioes': '1,2.5,3,-4,0.1,6'}}"]


def test_borda_texto_bool_none_e_niveis_vazios(caplog):
    caplog.set_level(logging.INFO)

    assert executar([[["12", [True, None]]], [[]]]) == "1,2,True,None,"  # "12" sai digito por digito
    assert executar([]) == ""
    assert executar(((((7,),),),)) == "7"
    assert caplog.messages[0] == "Config: {'mundo': {'regioes': '1,2,True,None,'}}"


def test_invalido_ultimo_nivel_que_nao_e_sequencia():
    with pytest.raises(TypeError):
        executar([[[1, 2]]])
