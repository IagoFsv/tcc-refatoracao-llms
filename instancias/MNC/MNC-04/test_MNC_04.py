"""Testes da instancia MNC-04: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode quebrar a tabela de permissoes
em partes nomeadas ou monta-la de outro jeito; o que nao pode mudar e o
conteudo de cada permissao (variaveis de ambiente e volumes) e o erro diante
de servico desconhecido.
"""

import pytest

from MNC_04 import executar


def test_tipico_permissao_com_ambiente_e_volume():
    assert executar("lnd") == {
        "env": {
            "LND_IP": "${LND_IP}",
            "LND_GRPC_PORT": "${LND_GRPC_PORT}",
            "LND_REST_PORT": "${LND_REST_PORT}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}",
        },
        "volumes": ["${LND_DATA_DIR}:/lnd:ro"],
    }


def test_borda_permissao_so_com_ambiente_sem_volumes():
    permissao = executar("bitcoind")

    assert "volumes" not in permissao
    assert permissao == {
        "env": {
            "BITCOIN_IP": "${BITCOIN_IP}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}",
            "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
            "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
            "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
            "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
            "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}",
        },
    }


def test_invalido_servico_desconhecido():
    with pytest.raises(KeyError):
        executar("electrs")
