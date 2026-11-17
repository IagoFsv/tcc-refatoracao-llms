from dataclasses import dataclass, asdict
from types import SimpleNamespace

_scopes = []


class _Node:
    """Graph node: description of the operation and shape of the result, if known."""

    def __init__(self, description, shape=None):
        self.description = description
        self.shape = shape

    def __add__(self, other):
        return _Node(("add", _current_scope(), self.description, other.description), self.shape)


def _current_scope():
    return "/".join(_scopes)


class _NameScope:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        _scopes.append(self.name)
        return self.name

    def __exit__(self, *exc):
        _scopes.pop()
        return False


def _variable(initial_value):
    return _Node(("Variable", _current_scope(), initial_value.description), initial_value.shape)


def _truncated_normal(shape, mean=0.0, stddev=1.0):
    return _Node(("truncated_normal", tuple(shape), mean, stddev), tuple(shape))


def _constant(value, dtype=None, shape=None):
    return _Node(("constant", value, tuple(shape)), tuple(shape))


def _conv2d(input, filter, strides, padding):
    if filter.shape is not None and len(filter.shape) != 4:
        raise ValueError(f"Shape must be rank 4 but is rank {len(filter.shape)}")
    return _Node(("conv2d", _current_scope(), input.description, filter.description,
                  tuple(strides), padding))


def _max_pool(value, ksize, strides, padding):
    return _Node(("max_pool", _current_scope(), value.description, tuple(ksize),
                  tuple(strides), padding))


def _relu(features):
    return _Node(("relu", _current_scope(), features.description))


tf = SimpleNamespace(
    Variable=_variable,
    truncated_normal=_truncated_normal,
    constant=_constant,
    name_scope=_NameScope,
    nn=SimpleNamespace(conv2d=_conv2d, max_pool=_max_pool, relu=_relu),
)


@dataclass
class Layer:
    input_shape: tuple
    num_input_channels: int
    num_filters: int
    filter_shape: tuple
    pool_shape: tuple
    name: str


def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))


def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))


def create_convolutional_layer(layer: Layer):
    with tf.name_scope(layer.name):
        weights = create_weights(shape=layer.filter_shape)
        biases = create_biases(layer.num_filters)
        input_node = _Node(("input", tuple(layer.input_shape)), tuple(layer.input_shape))
        layer_node = tf.nn.conv2d(input=input_node, filter=weights, strides=[
                                 1, 1, 1, 1], padding='SAME')
        layer_node += biases
        layer_node = tf.nn.max_pool(
            value=layer_node, ksize=layer.pool_shape, strides=layer.pool_shape, padding='SAME')
        layer_node = tf.nn.relu(layer_node)
        return layer_node.description


def run(layer: Layer):
    """Public entry point of this unit.

    layer: input_shape, num_input_channels, num_filters, filter_shape,
    pool_shape and name. Returns the description of the final graph node.
     """
    return create_convolutional_layer(layer)
