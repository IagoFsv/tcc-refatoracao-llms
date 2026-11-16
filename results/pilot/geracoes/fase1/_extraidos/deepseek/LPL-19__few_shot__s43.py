from dataclasses import dataclass, asdict

@dataclass
class Camada:
    formato_entrada: tuple
    num_input_channels: int
    num_filters: int
    filter_shape: tuple
    pool_shape: tuple
    name: str

def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))

def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))

def create_convolutional_layer(input, camada: Camada):
    with tf.name_scope(camada.name):
        weights = create_weights(shape=camada.filter_shape)
        biases = create_biases(camada.num_filters)
        layer = tf.nn.conv2d(input=input, filter=weights, strides=[
                            1, 1, 1, 1], padding='SAME')
        layer += biases
        layer = tf.nn.max_pool(
            value=layer, ksize=camada.pool_shape, strides=camada.pool_shape, padding='SAME')
        layer = tf.nn.relu(layer)
        return layer

def executar(camada: Camada):
    entrada = _No(("entrada", tuple(camada.formato_entrada)), tuple(camada.formato_entrada))
    no = create_convolutional_layer(entrada, camada)
    return no.descricao
