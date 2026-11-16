from dataclasses import dataclass

@dataclass
class Dimensoes:
    num_classes: int
    input_size: int
    hidden_size: int
    num_layers: int

def executar(dimensoes: Dimensoes):
    modelo = BasicLSTM(
        dimensoes.num_classes,
        dimensoes.input_size,
        dimensoes.hidden_size,
        dimensoes.num_layers,
    )
    return _resumo(modelo)
