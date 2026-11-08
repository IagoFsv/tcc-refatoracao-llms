from dataclasses import dataclass, asdict

@dataclass
class Camada:
    formato_entrada: tuple
    num_input_channels: int
    num_filters: int
    filter_shape: tuple
    pool_shape: tuple
    name: str

def executar(camada: Camada):
    entrada = _No(("entrada", camada.formato_entrada), camada.formato_entrada)
    no = create_convolutional_layer(entrada, camada.num_input_channels, camada.num_filters, camada.filter_shape, camada.pool_shape, camada.name)
    return no.descricao
