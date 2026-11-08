permissions_env = {
    "LND_IP": "${LND_IP}",
    "LND_GRPC_PORT": "${LND_GRPC_PORT}",
    "LND_REST_PORT": "${LND_REST_PORT}",
    "BITCOIN_NETWORK": "${BITCOIN_NETWORK}"
}

permissions_volumes = ['${LND_DATA_DIR}:/lnd:ro']

permissions_bitcoind = {
    "BITCOIN_IP": "${BITCOIN_IP}",
    "BITCOIN_NETWORK": "${BITCOIN_NETWORK}",
    "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
    "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
    "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
    "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
    "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}"
}

def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    if nome == "lnd":
        return permissions_env, permissions_volumes
    elif nome == "bitcoind":
        return permissions_bitcoind
