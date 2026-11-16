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
    elif elements in range(7, 12):
        return get_layout_size_for_range(elements)
    elif elements in range(12, 36):
        return get_layout_size_for_range(elements)
    elif elements in range(36, 64):
        return get_layout_size_for_range(elements)
    elif elements > 63:
        return get_layout_size_for_golden_ratio(elements)
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')


def get_layout_size_for_range(elements):
    if elements in range(7, 13):
        return 6, 2
    elif elements in range(13, 25):
        return 6, 4
    elif elements in range(25, 31):
        return 6, 5
    elif elements in range(31, 36):
        return 7, 5
    elif elements in range(36, 43):
        return 7, 6
    elif elements in range(43, 50):
        return 7, 7
    elif elements in range(50, 57):
        return 7, 8
    elif elements in range(57, 64):
        return 7, 9
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')


def get_layout_size_for_golden_ratio(elements):
    phi = (1 + math.sqrt(5)) / 2
    short_edge = math.floor((math.sqrt(elements * phi)) / phi)
    long_edge = math.ceil(elements / short_edge)
    return short_edge, long_edge


def executar(elementos):
    """Devolve (colunas, linhas) para o numero de elementos. Ponto de entrada publico desta unidade."""
    return get_layout_size(elementos)
