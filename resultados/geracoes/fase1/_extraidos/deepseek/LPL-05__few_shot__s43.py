from dataclasses import dataclass, asdict

@dataclass
class Dimensions:
    num_classes: int
    input_size: int
    hidden_size: int
    num_layers: int

def execute(dimensions: Dimensions):
    model = BasicLSTM(
        dimensions.num_classes,
        dimensions.input_size,
        dimensions.hidden_size,
        dimensions.num_layers,
    )
    return _summary(model)
