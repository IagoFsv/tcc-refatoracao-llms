def _get_layout_size_for_range(elements, min_cols, max_cols, min_rows, max_rows):
    if elements <= max_cols:
        return min_cols, 1
    elif elements <= max_cols * 2:
        return max_cols, 2
    elif elements <= max_cols * 3:
        return max_cols, 3
    else:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge

def get_layout_size(elements):
    if elements <= 12:
        return _get_layout_size_for_range(elements, 4, 4, 1, 3)
    elif elements <= 36:
        return _get_layout_size_for_range(elements, 6, 7, 3, 12)
    else:
        return _get_layout_size_for_range(elements, 7, 7, 12, float('inf'))

def executar(elementos):
    return get_layout_size(elementos)
