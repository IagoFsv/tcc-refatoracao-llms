"""Grid of columns and rows to lay out elements in landscape.

Public entry point: run(elements). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import math


def _get_layout_size_for_small_elements(elements):
    if elements <= 1:
        return 1, 1
    elif elements == 2:
        return 2, 1
    elif elements == 3:
        return 3, 1
    elif elements == 4:
        return 4, 1
    elif elements == 5:
        return 5, 1
    elif elements == 6:
        return 6, 1
    elif elements == 7:
        return 4, 2
    elif elements == 8:
        return 4, 2
    elif elements == 9:
        return 5, 2
    elif elements == 10:
        return 5, 2
    elif elements == 11:
        return 6, 2
    elif elements == 12:
        return 6, 2
    else:
        raise ValueError(f'Unsupported number of elements:  {elements}')


def _get_layout_size_for_large_elements(elements):
    phi = (1 + math.sqrt(5)) / 2
    short_edge = math.floor((math.sqrt(elements * phi)) / phi)
    long_edge = math.ceil(elements / short_edge)
    return short_edge, long_edge


def get_layout_size(elements):
    if elements <= 12:
        return _get_layout_size_for_small_elements(elements)
    else:
        return _get_layout_size_for_large_elements(elements)


def run(elements):
    """Returns  (columns, rows) for the number of elements. Public entry point of this unit."""
    return get_layout_size(elements)
