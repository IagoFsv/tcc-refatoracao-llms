def executar(camada):
    """camada: formato_entrada, num_input_channels, num_filters, filter_shape,
    pool_shape e name. Devolve a descricao do no final do grafo."""
    c = camada
    params = ConvolutionalLayerParams(c["formato_entrada"], c["num_input_channels"], c["num_filters"],
                                      c["filter_shape"], c["pool_shape"], c["name"])
    no = create_convolutional_layer(params)
    return no
