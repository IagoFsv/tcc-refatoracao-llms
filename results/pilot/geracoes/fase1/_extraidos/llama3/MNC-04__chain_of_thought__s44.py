class ServicePermission:
    def __init__(self, name, env, volumes):
        self.name = name
        self.env = env
        self.volumes = volumes

services = [
    ServicePermission("lnd", {"LND_IP": "${LND_IP}", "LND_GRPC_PORT": "${LND_GRPC_PORT}", ...}, ["${LND_DATA_DIR}:/lnd:ro"]),
    ServicePermission("bitcoind", {"BITCOIN_IP": "${BITCOIN_IP}", "BITCOIN_NETWORK": "${BITCOIN_NETWORK}", ...}, [...]),
]

def executar(nome):
    """Devolve a permissao de um servico. Ponto de entrada publico desta unidade."""
    for service in services:
        if service.name == nome:
            return service
    return None
