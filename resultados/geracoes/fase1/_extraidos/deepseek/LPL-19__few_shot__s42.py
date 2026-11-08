from dataclasses import dataclass, asdict

@dataclass
class Camada:
    formato_entrada: tuple
    num_input_channels: int
    num_filters: int
    filter_shape: tuple
    pool_shape: tuple
    name: str

@dataclass
class No:
    descricao: str
    formato: tuple = None

@dataclass
class EscopoDeNome:
    name: str

_escopos = []

def _escopo_atual():
    return "/".join(_escopos)

def _variable(initial_value):
    return No(("Variable", _escopo_atual(), initial_value.descricao), initial_value.formato)

def _truncated_normal(shape, mean=0.0, stddev=1.0):
    return No(("truncated_normal", tuple(shape), mean, stddev), tuple(shape))

def _constant(value, dtype=None, shape=None):
    return No(("constant", value, tuple(shape)), tuple(shape))

def _conv2d(input, filter, strides, padding):
    if filter.formato is not None and len(filter.formato) != 4:
        raise ValueError(f"Shape must be rank 4 but is rank {len(filter.formato)}")
    return No(("conv2d", _escopo_atual(), input.descricao, filter.descricao,
               tuple(strides), padding))

def _max_pool(value, ksize, strides, padding):
    return No(("max_pool", _escopo_atual(), value.descricao, tuple(ksize),
               tuple(strides), padding))

def _relu(features):
    return No(("relu", _escopo_atual(), features.descricao))

def create_weights(shape):
    return _variable(_truncated_normal(shape, stddev=0.05))

def create_biases(size):
    return _variable(_constant(0.05, shape=[size]))

def create_convolutional_layer(input, num_input_channels, num_filters, filter_shape, pool_shape, name):
    with EscopoDeNome(name):
        weights = create_weights(shape=filter_shape)
        biases = create_biases(num_filters)
        layer = _conv2d(input=input, filter=weights, strides=[1, 1, 1, 1], padding='SAME')
        layer += biases
        layer = _max_pool(value=layer, ksize=pool_shape, strides=pool_shape, padding='SAME')
        layer = _relu(layer)
        return layer

def executar(camada: Camada):
    c = camada
    entrada = No(("entrada", tuple(c.formato_entrada)), tuple(c.formato_entrada))
    no = create_convolutional_layer(entrada, c.num_input_channels, c.num_filters,
                                    c.filter_shape, c.pool_shape, c.name)
    return no.descricao
