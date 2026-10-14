"""Testes da instancia LPL-18: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
DQNAgent.__init__ num objeto, mudar a assinatura ou dividir o metodo, desde
que atualize a chamada dentro da unidade; o que nao pode mudar sao os oito
hiperparametros guardados no agente, a memoria (capacidade 1000, vazia),
as duas redes (com as mesmas dimensoes, objetos distintos, a alvo com os
pesos copiados da principal) e o erro diante de tamanho negativo.
"""

import pytest

from LPL_18 import executar


def _configuracao(**mudancas):
    base = {"input_size": 4, "n_actions": 2, "hidden_size": 24, "gamma": 0.95,
            "batch_size": 32, "epsilon": 1.0, "epsilon_min": 0.01, "epsilon_decay": 0.995}
    base.update(mudancas)
    return base


def _esperado(c):
    dimensoes = (c["input_size"], c["n_actions"], c["hidden_size"], c["gamma"])
    return {
        "hiperparametros": c,
        "memoria": (1000, 0),
        "redes": (dimensoes, dimensoes),
        "redes_distintas": True,
        "alvo_sincronizado": True,
    }


def test_tipico_agente_para_quatro_entradas_e_duas_acoes():
    c = _configuracao()

    assert executar(c) == _esperado(c)


def test_borda_exploracao_ja_no_minimo_e_lote_de_um():
    c = _configuracao(input_size=1, n_actions=1, hidden_size=1, batch_size=1,
                      epsilon=0.01, epsilon_min=0.01, epsilon_decay=1.0)

    assert executar(c) == _esperado(c)


def test_invalido_camada_oculta_negativa():
    with pytest.raises(RuntimeError):
        executar(_configuracao(hidden_size=-1))
