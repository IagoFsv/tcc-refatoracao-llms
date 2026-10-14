"""Montagem de uma camada convolucional num grafo de operacoes.

Ponto de entrada publico: executar(camada). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.

As operacoes (variavel, normal truncada, constante, convolucao, max pooling,
ReLU, soma e escopo de nome) sao versoes minimas que nao calculam nada: cada
uma devolve um no do grafo que registra a operacao, o escopo de nome em que
foi criada e as entradas. A convolucao recusa filtro que nao tenha 4
dimensoes, como a versao real.
"""

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


def executar(camada):
    """camada: formato_entrada, num_input_channels, num_filters, filter_shape,
    pool_shape e name. Devolve a descricao do no final do grafo."""
    c = camada
    entrada = _No(("entrada", tuple(c["formato_entrada"])), tuple(c["formato_entrada"]))
    no = create_convolutional_layer(entrada, c["num_input_channels"], c["num_filters"],
                                    c["filter_shape"], c["pool_shape"], c["name"])
    return no.descricao
