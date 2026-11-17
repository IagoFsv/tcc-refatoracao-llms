"""Grid of columns and rows to lay out elements in landscape.

Public entry point: run(elements). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import math


def get_layout_size(elements):
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
    elif is_within_range(elements, 13, 18):
        return 6, 3
    elif is_within_range(elements, 19, 24):
        return 6, 4
    elif is_within_range(elements, 25, 30):
        return 6, 5
    elif is_within_range(elements, 31, 35):
        return 7, 5
    elif is_within_range(elements, 36, 42):
        return 7, 6
    elif is_within_range(elements, 43, 49):
        return 7, 7
    elif is_within_range(elements, 50, 56):
        return 7, 8
    elif is_within_range(elements, 57, 63):
        return 7, 9
    elif is_within_range(elements, 64, 70):
        return 7, 10
    elif is_within_range(elements, 71, 77):
        return 7, 11
    elif is_within_range(elements, 78, 84):
        return 7, 12
    elif is_within_range(elements, 85, 91):
        return 7, 13
    elif elements > 91:
        return calculate_layout_size_for_large_elements(elements)
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')


def run(elements):
    """Returns (columns, rows) for the number of elements. Public entry point of this unit."""
    return get_layout_size(elements)


def is_within_range(value, start, end):
    return start <= value <= end


def calculate_layout_size_for_large_elements(elements):
    phi = (1 + math.sqrt(5)) / 2
    short_edge = math.floor((math.sqrt(elements * phi)) / phi)
    long_edge = math.ceil(elements / short_edge)
    return short_edge, long_edge
