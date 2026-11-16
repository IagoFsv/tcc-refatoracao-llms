from types import SimpleNamespace

_escopos = []


class _No:
    """No do grafo: descricao da operacao e formato do resultado, se conhecido."""

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


class ConvolutionalLayer:
    def __init__(self, formato_entrada, num_input_channels, num_filters, filter_shape, pool_shape, name):
        self.formato_entrada = formato_entrada
        self.num_input_channels = num_input_channels
        self.num_filters = num_filters
        self.filter_shape = filter_shape
        self.pool_shape = pool_shape
        self.name = name

    def __call__(self):
        weights = create_weights(shape=self.filter_shape)
        biases = create_biases(self.num_filters)
        layer = tf.nn.conv2d(input=tf.Variable(self.formato_entrada), filter=weights, strides=[
                             1, 1, 1, 1], padding='SAME')
        layer += biases
        layer = tf.nn.max_pool(
            value=layer, ksize=self.pool_shape, strides=self.pool_shape, padding='SAME')
        layer = tf.nn.relu(layer)
        return layer


def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))


def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))


def executar(camada):
    """camada: ConvolutionalLayer. Devolve a descricao do no final do grafo."""
    c = camada
    entrada = _No(("entrada", tuple(c.formato_entrada)), tuple(c.formato_entrada))
    no = entrada + c()
    return no.descricao

tf = SimpleNamespace(
    Variable=_variable,
    truncated_normal=_truncated_normal,
    constant=_constant,
    name_scope=_EscopoDeNome,
    nn=SimpleNamespace(conv2d=_conv2d, max_pool=_max_pool, relu=_relu),
)

executar(ConvolutionalLayer(("image", 1, 28, 28), 1, 32, (5, 5), (1, 1), "layer1"))
