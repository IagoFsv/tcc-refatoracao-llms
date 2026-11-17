"""Grid of columns and rows to lay out elements in landscape.

Public entry point: run(elements). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import math


def get_columns(elements):
    if elements <= 1:
        return 1
    elif elements == 2:
        return 2
    elif elements in range(3, 7):
        return 3
    elif elements in range(8, 13):
        return 4
    elif elements in range(14, 25):
        return 5
    elif elements in range(26, 36):
        return 6
    elif elements in range(37, 50):
        return 7
    elif elements in range(51, 64):
        return 7
    elif elements in range(65, 78):
        return 7
    elif elements in range(79, 92):
        return 7
    elif elements > 91:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        return short_edge
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')


def get_rows(elements):
    if elements <= 1:
        return 1
    elif elements in range(2, 4):
        return 2
    elif elements in range(5, 7):
        return 2
    elif elements in range(8, 12):
        return 3
    elif elements in range(13, 19):
        return 3
    elif elements in range(20, 25):
        return 4
    elif elements in range(26, 31):
        return 5
    elif elements in range(32, 36):
        return 5
    elif elements in range(37, 43):
        return 6
    elif elements in range(44, 50):
        return 7
    elif elements in range(51, 57):
        return 8
    elif elements in range(58, 64):
        return 9
    elif elements in range(65, 71):
        return 10
    elif elements in range(72, 78):
        return 11
    elif elements in range(79, 85):
        return 12
    elif elements in range(86, 92):
        return 13
    elif elements > 91:
        return 7


def get_layout_size(elements):
    return get_columns(elements), get_rows(elements)


def run(elements):
    """Returns (columns, rows) for the number of elements. Public entry point of this unit."""
    return get_layout_size(elements)
