import math


def _get_column_count(elements):
    if elements <= 1:
        return 1
    elif elements <= 3:
        return 3
    elif elements <= 4:
        return 4
    else:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        return math.ceil(elements / short_edge)


def _get_row_count(elements, column_count):
    return math.ceil(elements / column_count)


def get_layout_size(elements):
    column_count = _get_column_count(elements)
    return column_count, _get_row_count(elements, column_count)


def run(elements):
    """Returns (columns, rows) for the number of elements. Public entry point of this unit."""
    return get_layout_size(elements)
