"""Grid of columns and rows to lay out elements in landscape.

Public entry point: run(elements). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import math


def _get_columns(elements):
    if elements <= 1:
        return 1
    elif elements in range(2, 7):
        return 3
    elif elements in range(7, 13):
        return 4
    elif elements in range(13, 20):
        return 5
    elif elements in range(20, 37):
        return 6
    else:
        phi = (1 + math.sqrt(5)) / 2
        return math.ceil(elements / math.floor((math.sqrt(elements * phi)) / phi))


def _get_rows(elements, columns):
    return math.ceil(elements / columns)


def run(elements):
    """Returns (columns, rows) for the number of elements. Public entry point of this unit."""
    columns = _get_columns(elements)
    rows = _get_rows(elements, columns)
    return columns, rows
