"""Tests for instance LPL-18: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
DQNAgent.__init__ into an object, change the signature or split the method,
as long as it updates the call inside the unit; what must not change are the
eight hyperparameters stored in the agent, the memory (capacity 1000, empty),
the two networks (same dimensions, distinct objects, the target with the
weights copied from the main one) and the error on a negative size.
"""

import pytest

from LPL_18 import run


def _configuration(**changes):
    base = {"input_size": 4, "n_actions": 2, "hidden_size": 24, "gamma": 0.95,
            "batch_size": 32, "epsilon": 1.0, "epsilon_min": 0.01, "epsilon_decay": 0.995}
    base.update(changes)
    return base


def _expected(c):
    dimensions = (c["input_size"], c["n_actions"], c["hidden_size"], c["gamma"])
    return {
        "hyperparameters": c,
        "memory": (1000, 0),
        "networks": (dimensions, dimensions),
        "distinct_networks": True,
        "target_in_sync": True,
    }


def test_typical_agent_for_four_inputs_and_two_actions():
    c = _configuration()

    assert run(c) == _expected(c)


def test_edge_exploration_already_at_minimum_and_batch_of_one():
    c = _configuration(input_size=1, n_actions=1, hidden_size=1, batch_size=1,
                       epsilon=0.01, epsilon_min=0.01, epsilon_decay=1.0)

    assert run(c) == _expected(c)


def test_invalid_negative_hidden_layer():
    with pytest.raises(RuntimeError):
        run(_configuration(hidden_size=-1))
