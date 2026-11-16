from types import SimpleNamespace

_scopes = []


class Node:
    def __init__(self, description, format=None):
        self.description = description
        self.format = format

    def __add__(self, other):
        return Node(("add", _current_scope(), self.description, other.description), self.format)


def _current_scope():
    return "/".join(_scopes)


class Scope:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        _scopes.append(self.name)
        return self.name

    def __exit__(self, *exception):
        _scopes.pop()
        return False


def _variable(initial_value):
    return Node(("Variable", _current_scope(), initial_value.description), initial_value.format)


def _truncated_normal(shape, mean=0.0, stddev=1.0):
    return Node(("truncated_normal", tuple(shape), mean, stddev), tuple(shape))


def _constant(value, dtype=None, shape=None):
    return Node(("constant", value, tuple(shape)), tuple(shape))


def _conv2d(input, filter, strides, padding):
    if filter.format is not None and len(filter.format) != 4:
        raise ValueError(f"Shape must be rank 4 but is rank {len(filter.format)}")
    return Node(("conv2d", _current_scope(), input.description, filter.description,
                 tuple(strides), padding))


def _max_pool(value, ksize, strides, padding):
    return Node(("max_pool", _current_scope(), value.description, tuple(ksize),
                 tuple(strides), padding))


def _relu(features):
    return Node(("relu", _current_scope(), features.description))


tf = SimpleNamespace(
    Variable=_variable,
    truncated_normal=_truncated_normal,
    constant=_constant,
    name_scope=Scope,
    nn=SimpleNamespace(conv2d=_conv2d, max_pool=_max_pool, relu=_relu),
)


def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))


def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))


def create_convolutional_layer(input, num_input_channels, num_filters, filter_shape, pool_shape, name):
    with tf.name_scope(name):
        weights = create_weights(shape=filter_shape)
        biases = create_biases(num_filters)
        layer = tf.nn.conv2d(input=input, filter=weights, strides=[
                            1, 1, 1, 1], padding='SAME')
        layer += biases
        layer = tf.nn.max_pool(
            value=layer, ksize=pool_shape, strides=pool_shape, padding='SAME')
        layer = tf.nn.relu(layer)
        return layer


def execute(layer):
    c = layer
    input = Node(("input", tuple(c["format_input"])), tuple(c["format_input"]))
    node = create_convolutional_layer(input, c["num_input_channels"], c["num_filters"],
                                      c["filter_shape"], c["pool_shape"], c["name"])
    return node.description
