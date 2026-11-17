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


class LayerParams:
    def __init__(self, input_shape, num_input_channels, num_filters, filter_shape, pool_shape, name):
        self.input_shape = input_shape
        self.num_input_channels = num_input_channels
        self.num_filters = num_filters
        self.filter_shape = filter_shape
        self.pool_shape = pool_shape
        self.name = name


def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))


def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))


def create_convolutional_layer(layer_params: LayerParams):
    with tf.name_scope(layer_params.name):
        weights = create_weights(shape=layer_params.filter_shape)
        biases = create_biases(layer_params.num_filters)
        layer = tf.nn.conv2d(input=layer_params.input_shape, filter=weights, strides=[
                            1, 1, 1, 1], padding='SAME')
        layer += biases
        layer = tf.nn.max_pool(
            value=layer, ksize=layer_params.pool_shape, strides=layer_params.pool_shape, padding='SAME')
        layer = tf.nn.relu(layer)
        return layer


def run(layer):
    """Public entry point of this unit.

    layer: input_shape, num_input_channels, num_filters, filter_shape,
    pool_shape and name. Returns the description of the final graph node.
    """
    c = LayerParams(**layer)
    input_node = _Node(("input", tuple(c.input_shape)), tuple(c.input_shape))
    node = create_convolutional_layer(c)
    return node.description
