"""Tests for instance LPL-05: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of __init__
into an object, change the signature or split the method, as long as it
updates the call inside the unit; what must not change are the
hyperparameters stored in the model, the registered sublayers (name and
configuration) and the error on a hidden size of zero.

The sublayer names (lstm, fc_1, fc_2, relu) are pinned because they are the
keys of the state_dict, which the original program saves to disk. The
registration order is not pinned.
"""

import pytest

from LPL_05 import run


def _expected_layers(num_classes, input_size, hidden_size, num_layers):
    return {
        "lstm": ("LSTM", input_size, hidden_size, num_layers, True, True),
        "fc_1": ("Linear", hidden_size, 32, True),
        "fc_2": ("Linear", 32, num_classes, True),
        "relu": ("ReLU", False),
    }


def test_typical_alphabet_with_two_layers():
    dimensions = {"num_classes": 27, "input_size": 27, "hidden_size": 64, "num_layers": 2}

    hyperparameters, layers = run(dimensions)

    assert hyperparameters == dimensions
    assert layers == _expected_layers(27, 27, 64, 2)


def test_edge_smallest_valid_dimensions():
    dimensions = {"num_classes": 1, "input_size": 1, "hidden_size": 1, "num_layers": 1}

    hyperparameters, layers = run(dimensions)

    assert hyperparameters == dimensions
    assert layers == _expected_layers(1, 1, 1, 1)


def test_invalid_hidden_size_zero():
    with pytest.raises(ValueError):
        run({"num_classes": 27, "input_size": 27, "hidden_size": 0, "num_layers": 2})
