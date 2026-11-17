"""Grid of columns and rows to lay out elements in landscape.

Public entry point: run(elements). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import math


def _calculate_columns(elements):
    if elements <= 1:
        return 1
    elif elements == 2 or elements == 3 or elements == 4:
        return 4
    elif elements == 5 or elements == 6 or elements == 7 or elements == 8 or elements == 9 or elements == 10:
        return 5
    elif elements == 11 or elements == 12:
        return 6
    elif elements in range(13, 19):
        return 6
    elif elements in range(19, 36):
        return 7
    elif elements in range(36, 71):
        return 7
    elif elements in range(71, 92):
        return 7
    else:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return long_edge


def _calculate_rows(elements):
    if elements <= 1:
        return 1
    elif elements in range(2, 7):
        return 1
    elif elements in range(8, 15):
        return 2
    elif elements in range(16, 29):
        return 3
    elif elements in range(30, 43):
        return 4
    elif elements in range(44, 57):
        return 5
    elif elements in range(58, 71):
        return 6
    elif elements in range(72, 85):
        return 7
    elif elements in range(86, 92):
        return 8
    else:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return long_edge


def run(elements):
    """Returns (columns, rows) for the number of elements. Public entry point of this unit."""
    columns = _calculate_columns(elements)
    rows = _calculate_rows(elements)
    return columns, rows
