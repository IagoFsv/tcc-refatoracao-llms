"""Testes da instancia LPL-19: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
create_convolutional_layer num objeto, tirar o que nao e usado, mudar a
assinatura ou dividir a funcao, desde que atualize a chamada dentro da
unidade; o que nao pode mudar e o grafo montado (operacoes, entradas,
argumentos e escopo de nome de cada uma) e o erro diante de filtro que nao
tem 4 dimensoes.

O grafo esperado: relu(max_pool(conv2d(entrada, pesos) + vies)), tudo dentro
do escopo com o nome da camada; pesos sao uma variavel com normal truncada
(desvio 0.05) no formato do filtro, e o vies uma variavel constante 0.05 com
um valor por filtro.
"""

import pytest

from LPL_19 import executar


def _grafo(entrada, filtro, num_filters, pool, nome):
    pesos = ("Variable", nome, ("truncated_normal", tuple(filtro), 0.0, 0.05))
    vies = ("Variable", nome, ("constant", 0.05, (num_filters,)))
    conv = ("conv2d", nome, ("entrada", tuple(entrada)), pesos, (1, 1, 1, 1), "SAME")
    soma = ("add", nome, conv, vies)
    pool_ = ("max_pool", nome, soma, tuple(pool), tuple(pool), "SAME")
    return ("relu", nome, pool_)


def test_tipico_primeira_camada_para_imagens_28x28():
    camada = {"formato_entrada": [None, 28, 28, 1], "num_input_channels": 1,
              "num_filters": 32, "filter_shape": [5, 5, 1, 32],
              "pool_shape": [1, 2, 2, 1], "name": "layer_conv1"}

    assert executar(camada) == _grafo([None, 28, 28, 1], [5, 5, 1, 32], 32,
                                      [1, 2, 2, 1], "layer_conv1")


def test_borda_um_filtro_1x1_sem_reducao_no_pooling():
    camada = {"formato_entrada": [1, 4, 4, 3], "num_input_channels": 3,
              "num_filters": 1, "filter_shape": [1, 1, 3, 1],
              "pool_shape": [1, 1, 1, 1], "name": "minima"}

    assert executar(camada) == _grafo([1, 4, 4, 3], [1, 1, 3, 1], 1, [1, 1, 1, 1], "minima")


def test_invalido_filtro_com_duas_dimensoes():
    # E o formato que o create_model do arquivo original usa.
    camada = {"formato_entrada": [None, 28, 28, 1], "num_input_channels": 1,
              "num_filters": 32, "filter_shape": [5, 5],
              "pool_shape": [2, 2], "name": "layer_conv1"}

    with pytest.raises(ValueError):
        executar(camada)
