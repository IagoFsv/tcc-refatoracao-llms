"""Tests for instance LPL-02: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of train
into an object, change the signature or split the function, as long as it
updates the call inside the unit; what must not change is the loss, the
accuracy, the final state of the model and the error on an empty dataset.

Arithmetic of the typical test (3 classes, initial bias zero, rate 0.5):
  batch 1: gets the 1st sample right, the 2nd wrong (predicts 1, was 2).
           Mean loss 0.5. Gradient [0, 0.5, -0.5], bias becomes
           [0, -0.25, 0.25].
  batch 2: with the new bias it gets the 1st sample right (without the step
           of batch 1, the tie between classes 1 and 2 would give class 1,
           wrong) and the 2nd wrong (predicts 2, was 0). Mean loss 0.625.
           Gradient [-0.5, 0, 0.5] (only from batch 2: the gradient is
           zeroed between batches), bias becomes [0.25, -0.25, 0].
  loss: (0.5 + 0.625) / 4 samples = 0.28125. The original adds up the batch
  means and divides by the number of samples; pinned as it is.
  accuracy: 2 hits out of 4 = 50.0.
"""

import pytest

from LPL_02 import run


def test_typical_two_batches_with_hits_and_misses():
    batches = [
        ([[3, 1, 0], [0, 2, 1]], [0, 2]),
        ([[1, 2, 2], [0, 0, 1]], [2, 0]),
    ]

    loss, accuracy, bias, training = run(batches)

    assert loss == pytest.approx(0.28125)
    assert accuracy == pytest.approx(50.0)
    assert bias == pytest.approx([0.25, -0.25, 0.0])
    assert training is True


def test_edge_one_batch_all_right_leaves_the_model_unchanged():
    loss, accuracy, bias, training = run([([[5, 1, 0], [0, 0, 4]], [0, 2])])

    assert loss == pytest.approx(0.0)
    assert accuracy == pytest.approx(100.0)
    assert bias == pytest.approx([0.0, 0.0, 0.0])
    assert training is True


def test_invalid_empty_dataset():
    with pytest.raises(ZeroDivisionError):
        run([])
