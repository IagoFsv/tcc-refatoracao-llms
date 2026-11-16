permissions_common = {
    "env": {
        "BITCOIN_NETWORK": "${BITCOIN_NETWORK}"
    }
}

permissions_lnd = {
    "env": {
        "LND_IP": "${LND_IP}",
        "LND_GRPC_PORT": "${LND_GRPC_PORT}",
        "LND_REST_PORT": "${LND_REST_PORT}",
        **permissions_common["env"]
    },
    "volumes": [
        '${LND_DATA_DIR}:/lnd:ro'
    ]
}

permissions_bitcoind = {
    "env": {
        "BITCOIN_IP": "${BITCOIN_IP}",
        "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
        "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
        "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
        "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
        "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}",
        **permissions_common["env"]
    }
}

permissions = {
    "lnd": permissions_lnd,
    "bitcoind": permissions_bitcoind
}

def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    return permissions[nome]
