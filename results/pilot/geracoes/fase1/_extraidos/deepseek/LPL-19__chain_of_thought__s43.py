from types import SimpleNamespace

_escopos = []


class _No:
    def __init__(self, descricao, formato=None):
        self.descricao = descricao
        self.formato = formato

    def __add__(self, outro):
        return _No(("add", _escopo_atual(), self.descricao, outro.descricao), self.formato)


def _escopo_atual():
    return "/".join(_escopos)


class _EscopoDeNome:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        _escopos.append(self.name)
        return self.name

    def __exit__(self, *excecao):
        _escopos.pop()
        return False


def _variable(initial_value):
    return _No(("Variable", _escopo_atual(), initial_value.descricao), initial_value.formato)


def _truncated_normal(shape, mean=0.0, stddev=1.0):
    return _No(("truncated_normal", tuple(shape), mean, stddev), tuple(shape))


def _constant(value, dtype=None, shape=None):
    return _No(("constant", value, tuple(shape)), tuple(shape))


def _conv2d(input, filter, strides, padding):
    if filter.formato is not None and len(filter.formato) != 4:
        raise ValueError(f"Shape must be rank 4 but is rank {len(filter.formato)}")
    return _No(("conv2d", _escopo_atual(), input.descricao, filter.descricao,
                tuple(strides), padding))


def _max_pool(value, ksize, strides, padding):
    return _No(("max_pool", _escopo_atual(), value.descricao, tuple(ksize),
                tuple(strides), padding))


def _relu(features):
    return _No(("relu", _escopo_atual(), features.descricao))


tf = SimpleNamespace(
    Variable=_variable,
    truncated_normal=_truncated_normal,
    constant=_constant,
    name_scope=_EscopoDeNome,
    nn=SimpleNamespace(conv2d=_conv2d, max_pool=_max_pool, relu=_relu),
)


class ConvolutionalLayerParameters:
    def __init__(self, input, num_input_channels, num_filters, filter_shape, pool_shape, name):
        self.input = input
        self.num_input_channels = num_input_channels
        self.num_filters = num_filters
        self.filter_shape = filter_shape
        self.pool_shape = pool_shape
        self.name = name


def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))


def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))


def create_convolutional_layer(params: ConvolutionalLayerParameters):
    with tf.name_scope(params.name):
        weights = create_weights(shape=params.filter_shape)
        biases = create_biases(params.num_filters)
        layer = tf.nn.conv2d(input=params.input, filter=weights, strides=[
                            1, 1, 1, 1], padding='SAME')
        layer += biases
        layer = tf.nn.max_pool(
            value=layer, ksize=params.pool_shape, strides=params.pool_shape, padding='SAME')
        layer = tf.nn.relu(layer)
        return layer


def executar(camada):
    c = camada
    entrada = _No(("entrada", tuple(c["formato_entrada"])), tuple(c["formato_entrada"]))
    params = ConvolutionalLayerParameters(
        input=entrada,
        num_input_channels=c["num_input_channels"],
        num_filters=c["num_filters"],
        filter_shape=c["filter_shape"],
        pool_shape=c["pool_shape"],
        name=c["name"]
    )
    no = create_convolutional_layer(params)
    return no.descricao
