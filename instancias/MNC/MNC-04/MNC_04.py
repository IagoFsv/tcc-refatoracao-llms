"""Permissoes de servicos usadas na geracao de arquivos de composicao de conteineres.

Ponto de entrada publico: executar(nome). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

permissions = {
    "lnd": {
        "env": {
            "LND_IP": "${LND_IP}",
            "LND_GRPC_PORT": "${LND_GRPC_PORT}",
            "LND_REST_PORT": "${LND_REST_PORT}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}"
        },
        "volumes": [
            '${LND_DATA_DIR}:/lnd:ro'
        ]
    },
    "bitcoind": {
        "env": {
            "BITCOIN_IP":       "${BITCOIN_IP}",
            "BITCOIN_NETWORK":  "${BITCOIN_NETWORK}",
            "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
            "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
            "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
            "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
            "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}"
        }
    }
}


def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    return permissions[nome]
