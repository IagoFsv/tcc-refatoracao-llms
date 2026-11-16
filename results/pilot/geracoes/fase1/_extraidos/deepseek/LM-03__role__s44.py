import math

def get_layout_size(elements):
    if elements <= 1:
        return 1, 1
    elif elements in [2, 3, 4, 5, 6]:
        return elements, 1
    elif elements in range(7, 13):
        return 4, 2
    elif elements in range(13, 19):
        return 6, 3
    elif elements in range(19, 25):
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
    elif elements in range(64, 71):
        return 7, 10
    elif elements in range(71, 78):
        return 7, 11
    elif elements in range(78, 85):
        return 7, 12
    elif elements in range(85, 92):
        return 7, 13
    else:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge

def executar(elementos):
    """Devolve uma tupla (colunas, linhas) para o número de elementos. Ponto de entrada público desta unidade."""
    return get_layout_size(elementos)
