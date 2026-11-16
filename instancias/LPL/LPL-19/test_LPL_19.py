"""Tests for instance LPL-19: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
create_convolutional_layer into an object, drop what is unused, change the
signature or split the function, as long as it updates the call inside the
unit; what must not change is the graph that is built (operations, inputs,
arguments and name scope of each one) and the error on a filter that does
not have 4 dimensions.

The expected graph: relu(max_pool(conv2d(input, weights) + bias)), all inside
the scope named after the layer; the weights are a variable with a truncated
normal (stddev 0.05) in the filter shape, and the bias a variable with the
constant 0.05, one value per filter.
"""

import pytest

from LPL_19 import run


def _graph(input_shape, filter_shape, num_filters, pool, name):
    weights = ("Variable", name, ("truncated_normal", tuple(filter_shape), 0.0, 0.05))
    bias = ("Variable", name, ("constant", 0.05, (num_filters,)))
    conv = ("conv2d", name, ("input", tuple(input_shape)), weights, (1, 1, 1, 1), "SAME")
    total = ("add", name, conv, bias)
    pooled = ("max_pool", name, total, tuple(pool), tuple(pool), "SAME")
    return ("relu", name, pooled)


def test_typical_first_layer_for_28x28_images():
    layer = {"input_shape": [None, 28, 28, 1], "num_input_channels": 1,
             "num_filters": 32, "filter_shape": [5, 5, 1, 32],
             "pool_shape": [1, 2, 2, 1], "name": "layer_conv1"}

    assert run(layer) == _graph([None, 28, 28, 1], [5, 5, 1, 32], 32,
                                [1, 2, 2, 1], "layer_conv1")


def test_edge_one_1x1_filter_without_pooling_reduction():
    layer = {"input_shape": [1, 4, 4, 3], "num_input_channels": 3,
             "num_filters": 1, "filter_shape": [1, 1, 3, 1],
             "pool_shape": [1, 1, 1, 1], "name": "minimal"}

    assert run(layer) == _graph([1, 4, 4, 3], [1, 1, 3, 1], 1, [1, 1, 1, 1], "minimal")


def test_invalid_filter_with_two_dimensions():
    # It is the shape that create_model in the original file uses.
    layer = {"input_shape": [None, 28, 28, 1], "num_input_channels": 1,
             "num_filters": 32, "filter_shape": [5, 5],
             "pool_shape": [2, 2], "name": "layer_conv1"}

    with pytest.raises(ValueError):
        run(layer)
