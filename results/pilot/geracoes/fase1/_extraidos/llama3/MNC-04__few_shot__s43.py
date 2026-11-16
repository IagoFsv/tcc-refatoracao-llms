from dataclasses import dataclass

@dataclass
class EnvironmentVariable:
    name: str
    value: str

@dataclass
class Volume:
    host_path: str
    container_path: str

@dataclass
class ServicePermission:
    environment: dict[EnvironmentVariable]
    volumes: list[Volume]

permissions = [
    ServicePermission(
        environment={
            EnvironmentVariable("LND_IP", "${LND_IP}"),
            EnvironmentVariable("LND_GRPC_PORT", "${LND_GRPC_PORT}"),
            EnvironmentVariable("LND_REST_PORT", "${LND_REST_PORT}"),
            EnvironmentVariable("BITCOIN_NETWORK", "${BITCOIN_NETWORK}"),
        },
        volumes=[
            Volume("${LND_DATA_DIR}", "/lnd:ro")
        ]
    ),
    ServicePermission(
        environment={
            EnvironmentVariable("BITCOIN_IP", "${BITCOIN_IP}"),
            EnvironmentVariable("BITCOIN_NETWORK", "${BITCOIN_NETWORK}"),
            EnvironmentVariable("BITCOIN_P2P_PORT", "${BITCOIN_P2P_PORT}"),
            EnvironmentVariable("BITCOIN_RPC_PORT", "${BITCOIN_RPC_PORT}"),
            EnvironmentVariable("BITCOIN_RPC_USER", "${BITCOIN_RPC_USER}"),
            EnvironmentVariable("BITCOIN_RPC_PASS", "${BITCOIN_RPC_PASS}"),
            EnvironmentVariable("BITCOIN_RPC_AUTH", "${BITCOIN_RPC_AUTH}"),
        }
    )
]

def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    return next(permission for permission in permissions if permission.__dict__.get("name") == nome)
