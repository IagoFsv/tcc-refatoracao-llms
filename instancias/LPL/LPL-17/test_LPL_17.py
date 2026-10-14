"""Testes da instancia LPL-17: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
DQN.__init__ num objeto, mudar a assinatura ou dividir o metodo, desde que
atualize a chamada dentro da unidade; o que nao pode mudar sao as camadas
da rede (tipo, tamanhos e ordem), o otimizador Adam sobre os parametros da
propria rede, com a taxa padrao, a perda quadratica media, gamma e
n_actions, e o erro diante de tamanho negativo.

A ordem das camadas e fixada porque, numa sequencia, ela e a ordem do
calculo. Formato dos parametros de uma camada linear: pesos (saidas,
entradas) e vies (saidas,).
"""

import pytest

from LPL_17 import executar


def _esperado(input_size, n_actions, hidden_size, gamma):
    return {
        "camadas": [("Linear", input_size, hidden_size, True), ("ReLU", False),
                    ("Linear", hidden_size, n_actions, True)],
        "otimizador": ("Adam", [(hidden_size, input_size), (hidden_size,),
                                (n_actions, hidden_size), (n_actions,)], 0.001, True),
        "perda": ("MSELoss", "mean"),
        "gamma": gamma,
        "n_actions": n_actions,
    }


def test_tipico_rede_para_quatro_entradas_e_duas_acoes():
    resumo = executar({"input_size": 4, "n_actions": 2, "hidden_size": 16, "gamma": 0.99})

    assert resumo == _esperado(4, 2, 16, 0.99)


def test_borda_menores_tamanhos_e_gamma_zero():
    resumo = executar({"input_size": 1, "n_actions": 1, "hidden_size": 1, "gamma": 0})

    assert resumo == _esperado(1, 1, 1, 0)


def test_invalido_camada_oculta_negativa():
    with pytest.raises(RuntimeError):
        executar({"input_size": 4, "n_actions": 2, "hidden_size": -1, "gamma": 0.99})
