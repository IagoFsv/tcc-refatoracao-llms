PERMISSOES = {
    "LND": {"IP": "${LND_IP}", "GRPC_PORT": "${LND_GRPC_PORT}", "REST_PORT": "${LND_REST_PORT}", "NETWORK": "${BITCOIN_NETWORK}"},
    "VOLUMES": ["${LND_DATA_DIR}:/lnd:ro"],
    "BITCOIND": {
        "IP": "${BITCOIN_IP}",
        "NETWORK": "${BITCOIN_NETWORK}",
        "P2P_PORT": "${BITCOIN_P2P_PORT}",
        "RPC_PORT": "${BITCOIN_RPC_PORT}",
        "RPC_USER": "${BITCOIN_RPC_USER}",
        "RPC_PASS": "${BITCOIN_RPC_PASS}",
        "RPC_AUTH": "${BITCOIN_RPC_AUTH}"
    }
}

def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    return PERMISSOES.get(nome) if nome in PERMISSOES else {}
