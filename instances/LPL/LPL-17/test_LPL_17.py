"""Tests for instance LPL-17: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
DQN.__init__ into an object, change the signature or split the method, as
long as it updates the call inside the unit; what must not change are the
network layers (type, sizes and order), the Adam optimizer over the
network's own parameters with the default rate, the mean squared loss,
gamma and n_actions, and the error on a negative size.

The layer order is pinned because, in a sequence, it is the order of the
computation. Parameter shapes of a linear layer: weights (outputs, inputs)
and bias (outputs,).
"""

import pytest

from LPL_17 import run


def _expected(input_size, n_actions, hidden_size, gamma):
    return {
        "layers": [("Linear", input_size, hidden_size, True), ("ReLU", False),
                   ("Linear", hidden_size, n_actions, True)],
        "optimizer": ("Adam", [(hidden_size, input_size), (hidden_size,),
                               (n_actions, hidden_size), (n_actions,)], 0.001, True),
        "loss": ("MSELoss", "mean"),
        "gamma": gamma,
        "n_actions": n_actions,
    }


def test_typical_network_for_four_inputs_and_two_actions():
    summary = run({"input_size": 4, "n_actions": 2, "hidden_size": 16, "gamma": 0.99})

    assert summary == _expected(4, 2, 16, 0.99)


def test_edge_smallest_sizes_and_zero_gamma():
    summary = run({"input_size": 1, "n_actions": 1, "hidden_size": 1, "gamma": 0})

    assert summary == _expected(1, 1, 1, 0)


def test_invalid_negative_hidden_layer():
    with pytest.raises(RuntimeError):
        run({"input_size": 4, "n_actions": 2, "hidden_size": -1, "gamma": 0.99})
