permissions = {
    "lnd": LndPermissions(),
    "bitcoind": BitcoindPermissions()
}

class Permissions:
    def __init__(self, name):
        self.name = name

    def get(self):
        return getattr(self, self.name)

class LndPermissions(Permissions):
    def __init__(self):
        super().__init__("lnd")

    def lnd(self):
        return {
            "env": {
                "LND_IP": "${LND_IP}",
                "LND_GRPC_PORT": "${LND_GRPC_PORT}",
                "LND_REST_PORT": "${LND_REST_PORT}",
                "BITCOIN_NETWORK": "${BITCOIN_NETWORK}"
            },
            "volumes": [
                '${LND_DATA_DIR}:/lnd:ro'
            ]
        }

class BitcoindPermissions(Permissions):
    def __init__(self):
        super().__init__("bitcoind")

    def bitcoind(self):
        return {
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

def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    return permissions.get().get(nome)
