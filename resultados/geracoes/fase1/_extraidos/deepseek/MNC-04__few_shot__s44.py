from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Service:
    env: Dict[str, str] = field(default_factory=dict)
    volumes: List[str] = field(default_factory=list)

@dataclass
class Permissions:
    lnd: Service
    bitcoind: Service

permissions = Permissions(
    lnd=Service(
        env={
            "LND_IP": "${LND_IP}",
            "LND_GRPC_PORT": "${LND_GRPC_PORT}",
            "LND_REST_PORT": "${LND_REST_PORT}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}"
        },
        volumes=['${LND_DATA_DIR}:/lnd:ro']
    ),
    bitcoind=Service(
        env={
            "BITCOIN_IP": "${BITCOIN_IP}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}",
            "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
            "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
            "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
            "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
            "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}"
        }
    )
)

def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    if nome == "lnd":
        return permissions.lnd
    elif nome == "bitcoind":
        return permissions.bitcoind
