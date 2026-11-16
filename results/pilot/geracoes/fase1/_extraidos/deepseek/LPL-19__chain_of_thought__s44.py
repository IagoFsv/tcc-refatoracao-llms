from types import SimpleNamespace

_escopos = []


class No:
    def __init__(self, descricao, formato=None):
        self.descricao = descricao
        self.formato = formato

    def __add__(self, outro):
        return No(("add", _escopo_atual(), self.descricao, outro.descricao), self.formato)


def _escopo_atual():
    return "/".join(_escopos)


class EscopoDeNome:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        _escopos.append(self.name)
        return self.name

    def __exit__(self, *excecao):
        _escopos.pop()
        return False


class CamadaConvolucional:
    def __init__(self, formato_entrada, num_input_channels, num_filters, filter_shape, pool_shape, name):
        self.formato_entrada = formato_entrada
        self.num_input_channels = num_input_channels
        self.num_filters = num_filters
        self.filter_shape = filter_shape
        self.pool_shape = pool_shape
        self.name = name


def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))


def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))


def create_convolutional_layer(camada):
    with tf.name_scope(camada.name):
        weights = create_weights(shape=camada.filter_shape)
        biases = create_biases(camada.num_filters)
        layer = tf.nn.conv2d(input=camada.entrada, filter=weights, strides=[
                            1, 1, 1, 1], padding='SAME')
        layer += biases
        layer = tf.nn.max_pool(
            value=layer, ksize=camada.pool_shape, strides=camada.pool_shape, padding='SAME')
        layer = tf.nn.relu(layer)
        return layer


def executar(camada):
    c = CamadaConvolucional(**camada)
    c.entrada = No(("entrada", tuple(c.formato_entrada)), tuple(c.formato_entrada))
    no = create_convolutional_layer(c)
    return no.descricao
