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
    c = asdict(camada)
    entrada = _No(("entrada", tuple(c["formato_entrada"])), tuple(c["formato_entrada"]))
    no = create_convolutional_layer(entrada, c["num_input_channels"], c["num_filters"],
                                    c["filter_shape"], c["pool_shape"], c["name"])
    return no.descricao
