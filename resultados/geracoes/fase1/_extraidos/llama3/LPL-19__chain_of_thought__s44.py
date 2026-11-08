class Camada:
    def __init__(self, formato_entrada, num_input_channels, num_filters, filter_shape, pool_shape, name):
        self.formato_entrada = formato_entrada
        self.num_input_channels = num_input_channels
        self.num_filters = num_filters
        self.filter_shape = filter_shape
        self.pool_shape = pool_shape
        self.name = name

def executar(camada):
    entrada = _No(("entrada", tuple(camada.formato_entrada)), tuple(camada.formato_entrada))
    no = create_convolutional_layer(entrada, camada.num_input_channels, camada.num_filters,
                                    camada.filter_shape, camada.pool_shape, camada.name)
    return no.descricao
