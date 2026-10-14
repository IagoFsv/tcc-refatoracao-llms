"""Testes da instancia LPL-16: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
Transaction.__init__ num objeto, mudar a assinatura ou dividir o metodo,
desde que atualize a chamada dentro da unidade; o que nao pode mudar e a
representacao da transacao em dicionario, inclusive o hash.

O hash da transacao e o sha256 de str(sender) + str(receiver) +
str(amount) + str(timestamp).
"""

import hashlib

from LPL_16 import executar


def _sha(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def test_tipico_transferencia_entre_duas_pessoas():
    transacao = executar({"sender": "Alice", "receiver": "Bob", "amount": 100,
                          "timestamp": 1700000000.0})

    assert transacao == {
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 100,
        "timestamp": 1700000000.0,
        "hash": _sha("Alice" + "Bob" + "100" + "1700000000.0"),
    }


def test_borda_valor_zero_para_si_mesma():
    transacao = executar({"sender": "Alice", "receiver": "Alice", "amount": 0,
                          "timestamp": 0})

    assert transacao == {
        "sender": "Alice",
        "receiver": "Alice",
        "amount": 0,
        "timestamp": 0,
        "hash": _sha("Alice" + "Alice" + "0" + "0"),
    }


def test_invalido_dados_de_tipo_errado_sao_aceitos_sem_validacao():
    transacao = executar({"sender": None, "receiver": "Bob", "amount": -50,
                          "timestamp": "ontem"})

    assert transacao == {
        "sender": None,
        "receiver": "Bob",
        "amount": -50,
        "timestamp": "ontem",
        "hash": _sha("None" + "Bob" + "-50" + "ontem"),
    }
