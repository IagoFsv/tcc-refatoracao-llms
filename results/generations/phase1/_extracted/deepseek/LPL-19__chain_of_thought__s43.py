def run(layer):
    """Public entry point of this unit.

    layer: input_shape, num_input_channels, num_filters, filter_shape,
    pool_shape and name. Returns the description of the final graph node.
    """
    c = LayerConfig(layer["input_shape"], layer["num_input_channels"], layer["num_filters"],
                    layer["filter_shape"], layer["pool_shape"], layer["name"])
    input_node = _Node(("input", tuple(c.input_shape)), tuple(c.input_shape))
    c.input_node = input_node
    node = create_convolutional_layer(c)
    return node.description
