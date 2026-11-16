from dataclasses import dataclass, asdict

@dataclass
class Config:
    formato_entrada: tuple
    num_input_channels: int
    num_filters: int
    filter_shape: tuple
    pool_shape: tuple
    name: str

def executar(config: Config):
    entrada = _No(("entrada", config.formato_entrada), config.formato_entrada)
    no = create_convolutional_layer(entrada, config.num_input_channels, config.num_filters,
                                    config.filter_shape, config.pool_shape, config.name)
    return no.descricao
