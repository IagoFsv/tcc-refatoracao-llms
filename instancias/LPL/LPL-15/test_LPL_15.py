"""Testes da instancia LPL-15: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
Block.__init__ num objeto, mudar a assinatura ou dividir o metodo, desde que
atualize a chamada dentro da unidade; o que nao pode mudar e a
representacao do bloco em dicionario, inclusive o hash e o proof padrao
(None).

O hash do bloco e o sha256 de str(index) + str(timestamp) + os hashes das
transacoes + str(previous_hash) + str(proof). Cada transacao de apoio tem
como hash o sha256 da propria descricao.
"""

import hashlib

from LPL_15 import executar


def _sha(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def test_tipico_bloco_com_duas_transacoes_e_proof():
    campos = {"index": 1, "timestamp": 1700000000.0,
              "transacoes": ["Alice->Bob:100", "Bob->Carol:20"],
              "previous_hash": "abc123", "proof": 42}

    bloco = executar(campos)

    hashes = _sha("Alice->Bob:100") + _sha("Bob->Carol:20")
    assert bloco == {
        "hash": _sha("1" + "1700000000.0" + hashes + "abc123" + "42"),
        "index": 1,
        "timestamp": 1700000000.0,
        "transactions": [{"descricao": "Alice->Bob:100"}, {"descricao": "Bob->Carol:20"}],
        "previous_hash": "abc123",
        "proof": 42,
    }


def test_borda_bloco_inicial_sem_transacoes_e_sem_proof():
    bloco = executar({"index": 0, "timestamp": 1700000000.0, "transacoes": [],
                      "previous_hash": None})

    assert bloco == {
        "hash": _sha("0" + "1700000000.0" + "" + "None" + "None"),
        "index": 0,
        "timestamp": 1700000000.0,
        "transactions": [],
        "previous_hash": None,
        "proof": None,
    }


def test_invalido_dados_de_tipo_errado_sao_aceitos_sem_validacao():
    bloco = executar({"index": "primeiro", "timestamp": -1, "transacoes": [],
                      "previous_hash": 123, "proof": "x"})

    assert bloco == {
        "hash": _sha("primeiro" + "-1" + "" + "123" + "x"),
        "index": "primeiro",
        "timestamp": -1,
        "transactions": [],
        "previous_hash": 123,
        "proof": "x",
    }
