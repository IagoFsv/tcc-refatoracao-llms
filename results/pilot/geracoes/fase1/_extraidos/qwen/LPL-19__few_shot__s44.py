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
class ConvolutionalLayerParams:
    input: _No
    filter: _No
    strides: tuple
    padding: str

def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))

def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))

def create_convolutional_layer(input, filter, strides, padding):
    with tf.name_scope("convolutional_layer"):
        weights = create_weights(shape=filter.formato)
        biases = create_biases(num_filters)
        layer = tf.nn.conv2d(input=input, filter=weights, strides=[
                             1, 1, 1, 1], padding='SAME')
        layer += biases
        layer = tf.nn.max_pool(
            value=layer, ksize=pool_shape, strides=pool_shape, padding='SAME')
        layer = tf.nn.relu(layer)
        return layer

def executar(camada: Camada):
    """camada: formato_entrada, num_input_channels, num_filters, filter_shape,
    pool_shape e name. Devolve a descricao do no final do grafo."""
    c = camada
    entrada = _No(("entrada", tuple(c.formato_entrada)), tuple(c.formato_entrada))
    layer_params = ConvolutionalLayerParams(
        input=entrada,
        filter=_truncated_normal(c.filter_shape),
        strides=(1, 1, 1, 1),
        padding='SAME'
    )
    no = create_convolutional_layer(**asdict(layer_params))
    return no.descricao
