"""Grid of columns and rows to lay out elements in landscape.

Public entry point: run(elements). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import math

# Mapping from number of elements to layout size
layout_sizes = {
    1: (1, 1),
    2: (2, 1),
    3: (3, 1),
    4: (4, 1),
    5: (5, 1),
    6: (6, 1),
    7: (4, 2),
    8: (4, 2),
    9: (5, 2),
    10: (5, 2),
    11: (6, 2),
    12: (6, 2),
    # Add more mappings as needed
}

def run(elements):
    """Returns (columns, rows) for the number of elements. Public entry point of this unit."""
    if elements in layout_sizes:
        return layout_sizes[elements]
    elif elements > 91:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')
