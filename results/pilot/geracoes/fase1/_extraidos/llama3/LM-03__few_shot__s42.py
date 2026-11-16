def get_layout_size_for_small_numbers(elements):
    if elements in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        return {1: (1, 1), 2: (2, 1), 3: (3, 1), 4: (4, 1), 5: (5, 1), 6: (6, 1), 7: (4, 2), 8: (4, 2), 9: (5, 2), 10: (5, 2), 11: (6, 2), 12: (6, 2)}.get(elements)

def get_layout_size_for_large_numbers(elements):
    if elements in range(13, 91):
        return {i: (7, i) for i in range(3, 14)}.get(elements)

def get_layout_size_for_phi_layout(elements):
    if elements > 91:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge

def get_layout_size(elements):
    if elements <= 12:
        return get_layout_size_for_small_numbers(elements)
    elif elements <= 91:
        return get_layout_size_for_large_numbers(elements)
    else:
        return get_layout_size_for_phi_layout(elements)

def executar(elementos):
    return get_layout_size(elementos)
