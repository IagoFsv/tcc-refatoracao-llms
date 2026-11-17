"""Grid of columns and rows to lay out elements in landscape.

Public entry point: run(elements). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import math


def calculate_layout_size(elements):
    if elements <= 1:
        return 1, 1
    elif elements <= 6:
        return elements, 1
    elif elements <= 12:
        return 6, math.ceil(elements / 6)
    elif elements <= 18:
        return 6, 3
    elif elements <= 24:
        return 6, 4
    elif elements <= 30:
        return 6, 5
    elif elements <= 35:
        return 7, 5
    elif elements <= 42:
        return 7, 6
    elif elements <= 49:
        return 7, 7
    elif elements <= 56:
        return 7, 8
    elif elements <= 63:
        return 7, 9
    elif elements <= 70:
        return 7, 10
    elif elements <= 77:
        return 7, 11
    elif elements <= 84:
        return 7, 12
    elif elements <= 91:
        return 7, 13
    elif elements > 91:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')


def get_layout_size(elements):
    return calculate_layout_size(elements)


def run(elements):
    """Returns (columns, rows) for the number of elements. Public entry point of this unit."""
    return get_layout_size(elements)
