"""Service permissions used to generate container composition files.

Public entry point: run(name). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class EnvVars:
    LND_IP: str
    LND_GRPC_PORT: str
    LND_REST_PORT: str
    BITCOIN_NETWORK: str
    BITCOIN_IP: str
    BITCOIN_P2P_PORT: str
    BITCOIN_RPC_PORT: str
    BITCOIN_RPC_USER: str
    BITCOIN_RPC_PASS: str
    BITCOIN_RPC_AUTH: str

@dataclass
class Volumes:
    volumes: List[str]

@dataclass
class ServiceConfig:
    env: EnvVars
    volumes: Volumes

permissions: Dict[str, ServiceConfig] = {
    "lnd": ServiceConfig(
        env=EnvVars(
            LND_IP="${LND_IP}",
            LND_GRPC_PORT="${LND_GRPC_PORT}",
            LND_REST_PORT="${LND_REST_PORT}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}"
        ),
        volumes=Volumes(
            volumes=['${LND_DATA_DIR}:/lnd:ro']
        )
    ),
    "bitcoind": ServiceConfig(
        env=EnvVars(
            BITCOIN_IP="${BITCOIN_IP}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}",
            BITCOIN_P2P_PORT="${BITCOIN_P2P_PORT}",
            BITCOIN_RPC_PORT="${BITCOIN_RPC_PORT}",
            BITCOIN_RPC_USER="${BITCOIN_RPC_USER}",
            BITCOIN_RPC_PASS="${BITCOIN_RPC_PASS}",
            BITCOIN_RPC_AUTH="${BITCOIN_RPC_AUTH}"
        ),
        volumes=Volumes(
            volumes=[]
        )
    )
}

def run(name):
    """Returns the permission of a service. Public entry point of this unit."""
    return permissions[name]
