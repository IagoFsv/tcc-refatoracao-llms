import math

def get_layout_size(elements):
    if elements <= 1:
        return 1, 1
    elif elements <= 6:
        return elements, 1
    elif elements <= 12:
        return 6, 2
    elif elements <= 18:
        return 6, 3
    elif elements <= 24:
        return 6, 4
    elif elements <= 30:
        return 6, 5
    elif elements <= 36:
        return 7, 5
    elif elements <= 42:
        return 7, 6
    elif elements <= 48:
        return 7, 7
    elif elements <= 54:
        return 7, 8
    elif elements <= 60:
        return 7, 9
    elif elements <= 66:
        return 7, 10
    elif elements <= 72:
        return 7, 11
    elif elements <= 78:
        return 7, 12
    elif elements <= 84:
        return 7, 13
    elif elements > 84:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')

def executar(elementos):
    """Devolve (colunas, linhas) para o numero de elementos. Ponto de entrada publico desta unidade."""
    return get_layout_size(elementos)
