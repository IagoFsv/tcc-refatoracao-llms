"""Testes da instancia LPL-05: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
__init__ num objeto, mudar a assinatura ou dividir o metodo, desde que
atualize a chamada dentro da unidade; o que nao pode mudar sao os
hiperparametros guardados no modelo, as subcamadas registradas (nome e
configuracao) e o erro diante de tamanho oculto zero.

Os nomes das subcamadas (lstm, fc_1, fc_2, relu) sao fixados porque sao as
chaves do state_dict, que o programa original salva em disco. A ordem de
registro nao e fixada.
"""

import pytest

from LPL_05 import executar


def _camadas_esperadas(num_classes, input_size, hidden_size, num_layers):
    return {
        "lstm": ("LSTM", input_size, hidden_size, num_layers, True, True),
        "fc_1": ("Linear", hidden_size, 32, True),
        "fc_2": ("Linear", 32, num_classes, True),
        "relu": ("ReLU", False),
    }


def test_tipico_alfabeto_com_duas_camadas():
    dimensoes = {"num_classes": 27, "input_size": 27, "hidden_size": 64, "num_layers": 2}

    hiperparametros, camadas = executar(dimensoes)

    assert hiperparametros == dimensoes
    assert camadas == _camadas_esperadas(27, 27, 64, 2)


def test_borda_menores_dimensoes_validas():
    dimensoes = {"num_classes": 1, "input_size": 1, "hidden_size": 1, "num_layers": 1}

    hiperparametros, camadas = executar(dimensoes)

    assert hiperparametros == dimensoes
    assert camadas == _camadas_esperadas(1, 1, 1, 1)


def test_invalido_tamanho_oculto_zero():
    with pytest.raises(ValueError):
        executar({"num_classes": 27, "input_size": 27, "hidden_size": 0, "num_layers": 2})
