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
    elif elements in {7, 8}:
        return 4, 2
    elif elements in {9, 10}:
        return 5, 2
    elif elements in {11, 12}:
        return 6, 2
    elif 13 <= elements < 19:
        return 6, 3
    elif 19 <= elements < 25:
        return 6, 4
    elif 25 <= elements < 31:
        return 6, 5
    elif 31 <= elements < 36:
        return 7, 5
    elif 36 <= elements < 43:
        return 7, 6
    elif 43 <= elements < 50:
        return 7, 7
    elif 50 <= elements < 57:
        return 7, 8
    elif 57 <= elements < 64:
        return 7, 9
    elif 64 <= elements < 71:
        return 7, 10
    elif 71 <= elements < 78:
        return 7, 11
    elif 78 <= elements < 85:
        return 7, 12
    elif 85 <= elements < 92:
        return 7, 13
    elif elements > 91:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')

def executar(elementos):
    """Devolve (colunas, linhas) para o numero de elementos. Ponto de entrada publico desta unidade."""
    return get_layout_size(elementos)
