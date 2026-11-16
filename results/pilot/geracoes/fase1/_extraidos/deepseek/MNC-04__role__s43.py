def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    return permissions[nome]


def obter_permissoes_lnd():
    return {
        "env": {
            "LND_IP": "${LND_IP}",
            "LND_GRPC_PORT": "${LND_GRPC_PORT}",
            "LND_REST_PORT": "${LND_REST_PORT}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}"
        },
        "volumes": ['${LND_DATA_DIR}:/lnd:ro']
    }


def obter_permissoes_bitcoind():
    return {
        "env": {
            "BITCOIN_IP": "${BITCOIN_IP}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}",
            "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
            "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
            "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
            "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
            "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}"
        }
    }


permissions = {
    "lnd": obter_permissoes_lnd(),
    "bitcoind": obter_permissoes_bitcoind()
}
