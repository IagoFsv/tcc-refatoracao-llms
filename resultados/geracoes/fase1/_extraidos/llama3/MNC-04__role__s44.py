permissions = {
    "lnd": {"env": {}, "volumes": []},
    "bitcoind": {"env": {}, "volumes": []}
}

def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    return {
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
                "BITCOIN_IP": "${BITCOIN_IP}",
                "BITCOIN_NETWORK": "${BITCOIN_NETWORK}",
                "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
                "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
                "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
                "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
                "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}"
            }
        }
    }[nome]
