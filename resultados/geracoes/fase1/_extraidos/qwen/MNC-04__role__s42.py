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

def get_service_permissions(service_name):
    """Devolve as permissões de um serviço."""
    return permissions.get(service_name, {})

def executar(nome):
    """Devolve a permissão de um serviço. Ponto de entrada publico desta unidade."""
    return get_service_permissions(nome)
