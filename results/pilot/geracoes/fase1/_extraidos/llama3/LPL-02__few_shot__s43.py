from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Treino:
    lotes: List[tuple]

@dataclass
class Modelo:
    vies: List[float]
    grad: List[float]
    training: bool

@dataclass
class Perda:
    output: _Tensor
    target: _Tensor

@dataclass
class Otimizador:
    modelo: Modelo

def executar(treino: Treino):
    modelo = Modelo(vies=[0.0] * _NUM_CLASSES, grad=[0.0] * _NUM_CLASSES, training=False)
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in treino.lotes])
    perda, acuracia, modelo = train(modelo, "cpu", loader, Otimizador(modelo), _Perda)
    return perda, acuracia, modelo.vies, modelo.training

def train(
        model: Modelo, 
        device: str, 
        train_loader: DataLoader, 
        optimizer: Otimizador, 
        criterion: Perda
        )->tuple[float, float, Modelo]:
    # ...
