from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class EnvConfig:
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
class VolumeConfig:
    volumes: List[str]

@dataclass
class ServiceConfig:
    env: EnvConfig
    volumes: VolumeConfig = field(default_factory=VolumeConfig)

@dataclass
class Permissions:
    lnd: ServiceConfig
    bitcoind: ServiceConfig

permissions = Permissions(
    lnd=ServiceConfig(
        env=EnvConfig(
            LND_IP="${LND_IP}",
            LND_GRPC_PORT="${LND_GRPC_PORT}",
            LND_REST_PORT="${LND_REST_PORT}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}"
        ),
        volumes=VolumeConfig(
            volumes=['${LND_DATA_DIR}:/lnd:ro']
        )
    ),
    bitcoind=ServiceConfig(
        env=EnvConfig(
            BITCOIN_IP="${BITCOIN_IP}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}",
            BITCOIN_P2P_PORT="${BITCOIN_P2P_PORT}",
            BITCOIN_RPC_PORT="${BITCOIN_RPC_PORT}",
            BITCOIN_RPC_USER="${BITCOIN_RPC_USER}",
            BITCOIN_RPC_PASS="${BITCOIN_RPC_PASS}",
            BITCOIN_RPC_AUTH="${BITCOIN_RPC_AUTH}"
        )
    )
)

def executar(nome: str) -> Dict:
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    return permissions.__dict__.get(nome, {})
