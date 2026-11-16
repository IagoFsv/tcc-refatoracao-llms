import math


def get_layout_size(elements):
    if elements <= 1:
        return 1, 1
    elif elements in range(2, 12):
        return get_layout_size_for_range(elements)
    elif elements > 91:
        return get_layout_size_for_fibonacci(elements)
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')


def get_layout_size_for_range(elements):
    # código para elementos entre 2 e 12
    # ...

def get_layout_size_for_fibonacci(elements):
    phi = (1 + math.sqrt(5)) / 2
    short_edge = math.floor((math.sqrt(elements * phi)) / phi)
    long_edge = math.ceil(elements / short_edge)
    return short_edge, long_edge


def executar(elementos):
    """Devolve (colunas, linhas) para o numero de elementos. Ponto de entrada publico desta unidade."""
    return get_layout_size(elementos)
