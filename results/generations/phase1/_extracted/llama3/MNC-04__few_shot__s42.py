"""Service permissions used to generate container composition files.

Public entry point: run(name). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class Env:
    LND_IP: str
    LND_GRPC_PORT: str
    LND_REST_PORT: str
    BITCOIN_NETWORK: str

@dataclass
class Volume:
    source: str
    target: str
    mode: str

@dataclass
class Service:
    env: Env
    volumes: List[Volume] = field(default_factory=list)

permissions = {
    "lnd": Service(
        Env(
            LND_IP="${LND_IP}",
            LND_GRPC_PORT="${LND_GRPC_PORT}",
            LND_REST_PORT="${LND_REST_PORT}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}"
        ),
        volumes=["${LND_DATA_DIR}:/lnd:ro"]
    ),
    "bitcoind": Service(
        Env(
            BITCOIN_IP="${BITCOIN_IP}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}",
            BITCOIN_P2P_PORT="${BITCOIN_P2P_PORT}",
            BITCOIN_RPC_PORT="${BITCOIN_RPC_PORT}",
            BITCOIN_RPC_USER="${BITCOIN_RPC_USER}",
            BITCOIN_RPC_PASS="${BITCOIN_RPC_PASS}",
            BITCOIN_RPC_AUTH="${BITCOIN_RPC_AUTH}"
        )
    )
}

def run(name):
    """Returns the permission of a service. Public entry point of this unit."""
    return permissions[name]
