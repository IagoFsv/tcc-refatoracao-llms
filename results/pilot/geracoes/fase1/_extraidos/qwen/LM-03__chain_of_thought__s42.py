import math

def get_layout_size(elements):
    if elements <= 1:
        return 1, 1
    elif elements <= 12:
        return get_layout_for_small_elements(elements)
    elif elements <= 18:
        return get_layout_for_elements_in_range(elements, 13, 18, 6, 3)
    elif elements <= 24:
        return get_layout_for_elements_in_range(elements, 19, 24, 6, 4)
    elif elements <= 30:
        return get_layout_for_elements_in_range(elements, 25, 30, 6, 5)
    elif elements <= 35:
        return get_layout_for_elements_in_range(elements, 31, 35, 7, 5)
    elif elements <= 42:
        return get_layout_for_elements_in_range(elements, 36, 42, 7, 6)
    elif elements <= 49:
        return get_layout_for_elements_in_range(elements, 43, 49, 7, 7)
    elif elements <= 56:
        return get_layout_for_elements_in_range(elements, 50, 56, 7, 8)
    elif elements <= 63:
        return get_layout_for_elements_in_range(elements, 57, 63, 7, 9)
    elif elements <= 70:
        return get_layout_for_elements_in_range(elements, 64, 70, 7, 10)
    elif elements <= 77:
        return get_layout_for_elements_in_range(elements, 71, 77, 7, 11)
    elif elements <= 84:
        return get_layout_for_elements_in_range(elements, 78, 84, 7, 12)
    elif elements <= 91:
        return get_layout_for_elements_in_range(elements, 85, 91, 7, 13)
    elif elements > 91:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')

def get_layout_for_small_elements(elements):
    return elements, 1

def get_layout_for_elements_in_range(elements, start, end, short_edge, long_edge):
    if start <= elements <= end:
        return short_edge, long_edge
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')

def executar(elementos):
    """Devolve (colunas, linhas) para o numero de elementos. Ponto de entrada publico desta unidade."""
    return get_layout_size(elementos)
