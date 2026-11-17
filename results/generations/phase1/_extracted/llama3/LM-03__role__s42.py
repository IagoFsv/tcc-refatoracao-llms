"""Grid of columns and rows to lay out elements in landscape.

Public entry point: run(elements). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import math


def get_base_layout_size(elements):
    if elements <= 1:
        return 1, 1
    elif elements in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        return elements, 1
    elif elements in range(13, 36):
        return 6, math.ceil((elements - 12) / 6)
    elif elements in range(36, 64):
        return 7, math.ceil((elements - 36) / 7)
    elif elements in range(64, 91):
        return 7, math.ceil((elements - 64) / 7)
    elif elements > 91:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')


def get_layout_size(elements):
    return get_base_layout_size(elements)


def run(elements):
    """Returns (columns, rows) for the number of elements. Public entry point of this unit."""
    return get_layout_size(elements)
