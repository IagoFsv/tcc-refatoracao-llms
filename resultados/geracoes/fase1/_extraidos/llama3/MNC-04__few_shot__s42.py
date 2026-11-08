from dataclasses import dataclass

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
    volumes: List[Volume]

permissions = [
    Service(
        env=Env(
            LND_IP="${LND_IP}",
            LND_GRPC_PORT="${LND_GRPC_PORT}",
            LND_REST_PORT="${LND_REST_PORT}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}"
        ),
        volumes=[f"${LND_DATA_DIR}:/lnd:ro"]
    ),
    Service(
        env=Env(
            BITCOIN_IP="${BITCOIN_IP}",
            BITCOIN_NETWORK="${BITCOIN_NETWORK}",
            BITCOIN_P2P_PORT="${BITCOIN_P2P_PORT}",
            BITCOIN_RPC_PORT="${BITCOIN_RPC_PORT}",
            BITCOIN_RPC_USER="${BITCOIN_RPC_USER}",
            BITCOIN_RPC_PASS="${BITCOIN_RPC_PASS}",
            BITCOIN_RPC_AUTH="${BITCOIN_RPC_AUTH}"
        ),
        volumes=[]
    )
]

def executar(nome):
    return next((permission for permission in permissions if permission.env.__dict__.get('LND_IP') == nome), None)
