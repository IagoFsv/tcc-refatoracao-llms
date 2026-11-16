from dataclasses import dataclass, asdict

@dataclass
class Config:
    num_classes: int
    input_size: int
    hidden_size: int
    num_layers: int

def executar(config: Config):
    modelo = BasicLSTM(
        config.num_classes,
        config.input_size,
        config.hidden_size,
        config.num_layers,
    )
    return _resumo(modelo)
