"""Floating-point operation count of normalization layers.

Public entry point: run(input_shape, affine, input_index=0, affine_index=1).
Do not change its name or signature; the rest of the file may be freely
reorganized.
"""

import operator
from functools import reduce
from typing import Any, Callable, List


class _Argument:
    """Argument of a traced operation that exposes a shape."""

    def __init__(self, shape):
        self.shape = shape


def norm_flop_counter(affine_arg_index: int, input_arg_index: int) -> Callable:
    """
    Args:
        affine_arg_index: index of the affine argument in inputs
    """

    def norm_flop_jit(inputs: List[Any], outputs: List[Any]) -> int:
        """
        Count flops for norm layers.
        """
        # Inputs[0] contains the shape of the input.
        input_shape = inputs[input_arg_index].shape

        has_affine = True
        if hasattr(inputs[affine_arg_index], 'shape'):
            has_affine = inputs[affine_arg_index].shape is not None
        else:
            has_affine = inputs[affine_arg_index]

        assert 2 <= len(input_shape) <= 5, input_shape
        # 5 is just a rough estimate
        flop = reduce(operator.mul, input_shape) * (5 if has_affine else 4)
        return flop

    return norm_flop_jit


def run(input_shape, affine, input_index=0, affine_index=1):
    """Counts the operations of one normalization call. Public entry point of this unit.

    input_shape is the shape of the input tensor. affine is either a shape
    (wrapped in an object with a shape attribute, None meaning no weights) or
    a plain flag (True/False), as the traced arguments can be.
    """
    inputs = [None] * (max(input_index, affine_index) + 1)
    inputs[input_index] = _Argument(input_shape)
    if isinstance(affine, bool):
        inputs[affine_index] = affine
    else:
        inputs[affine_index] = _Argument(affine)
    return norm_flop_counter(affine_index, input_index)(inputs, [])
