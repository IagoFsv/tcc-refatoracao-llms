from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class EnvVars:
    LND_IP: str
    LND_GRPC_PORT: str
    LND_REST_PORT: str
    BITCOIN_NETWORK: str

@dataclass
class Volumes:
    volumes: List[str]

@dataclass
class ServiceConfig:
    env: EnvVars
    volumes: Volumes

@dataclass
class Permissions:
    lnd: ServiceConfig
    bitcoind: ServiceConfig

permissions = Permissions(
    lnd=ServiceConfig(
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
    bitcoind=ServiceConfig(
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
)

def executar(nome: str) -> Dict[str, Any]:
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    return permissions.__dict__.get(nome, {})
