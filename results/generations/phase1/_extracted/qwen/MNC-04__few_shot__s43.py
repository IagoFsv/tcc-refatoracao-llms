"""Service permissions used to generate container composition files.

Public entry point: run(name). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

class ServicePermission:
    def __init__(self, env, volumes):
        self.env = env
        self.volumes = volumes

class EnvVars:
    def __init__(self, LND_IP, LND_GRPC_PORT, LND_REST_PORT, BITCOIN_NETWORK):
        self.LND_IP = LND_IP
        self.LND_GRPC_PORT = LND_GRPC_PORT
        self.LND_REST_PORT = LND_REST_PORT
        self.BITCOIN_NETWORK = BITCOIN_NETWORK

class BitcoindEnvVars(EnvVars):
    def __init__(self, LND_IP, LND_GRPC_PORT, LND_REST_PORT, BITCOIN_NETWORK, BITCOIN_IP, BITCOIN_P2P_PORT, BITCOIN_RPC_PORT, BITCOIN_RPC_USER, BITCOIN_RPC_PASS, BITCOIN_RPC_AUTH):
        super().__init__(LND_IP, LND_GRPC_PORT, LND_REST_PORT, BITCOIN_NETWORK)
        self.BITCOIN_IP = BITCOIN_IP
        self.BITCOIN_P2P_PORT = BITCOIN_P2P_PORT
        self.BITCOIN_RPC_PORT = BITCOIN_RPC_PORT
        self.BITCOIN_RPC_USER = BITCOIN_RPC_USER
        self.BITCOIN_RPC_PASS = BITCOIN_RPC_PASS
        self.BITCOIN_RPC_AUTH = BITCOIN_RPC_AUTH

permissions = {
    "lnd": ServicePermission(
        env=EnvVars(
            LND_IP="${LND_IP}",
            LND_GRPC_PORT="${LND_GRPC_PORT}",
            LND_REST_PORT="${LND_REST_PORT}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}"
        ),
        volumes=["${LND_DATA_DIR}:/lnd:ro"]
    ),
    "bitcoind": ServicePermission(
        env=BitcoindEnvVars(
            LND_IP="${LND_IP}",
            LND_GRPC_PORT="${LND_GRPC_PORT}",
            LND_REST_PORT="${LND_REST_PORT}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}",
            BITCOIN_IP="${BITCOIN_IP}",
            BITCOIN_P2P_PORT="${BITCOIN_P2P_PORT}",
            BITCOIN_RPC_PORT="${BITCOIN_RPC_PORT}",
            BITCOIN_RPC_USER="${BITCOIN_RPC_USER}",
            BITCOIN_RPC_PASS="${BITCOIN_RPC_PASS}",
            BITCOIN_RPC_AUTH="${BITCOIN_RPC_AUTH}"
        ),
        volumes=[]
    )
}

def run(name):
    """Returns the permission of a service. Public entry point of this unit."""
    return permissions[name]
