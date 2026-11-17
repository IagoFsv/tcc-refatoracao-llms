"""Service permissions used to generate container composition files.

Public entry point: run(name). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

lnd_env = {
    "LND_IP": "${LND_IP}",
    "LND_GRPC_PORT": "${LND_GRPC_PORT}",
    "LND_REST_PORT": "${LND_REST_PORT}",
    "BITCOIN_NETWORK": "${BITCOIN_NETWORK}"
}

lnd_volumes = ['${LND_DATA_DIR}:/lnd:ro']

lnd_permissions = {
    "env": lnd_env,
    "volumes": lnd_volumes
}

bitcoind_env = {
    "BITCOIN_IP": "${BITCOIN_IP}",
    "BITCOIN_NETWORK": "${BITCOIN_NETWORK}",
    "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
    "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
    "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
    "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
    "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}"
}

permissions = {
    "lnd": lnd_permissions,
    "bitcoind": {"env": bitcoind_env}
}


def run(name):
    """Returns the permission of a service. Public entry point of this unit."""
    return permissions[name]
