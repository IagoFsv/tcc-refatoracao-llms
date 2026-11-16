def get_layout_size_base(elements):
    if elements <= 1:
        return 1, 1
    elif elements in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        return [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].index(elements) + 1, 1
    elif elements in range(13, 19):
        return 6, 3
    # ... (removi as condições restantes e criei novos métodos)

def get_layout_size_phi(elements):
    phi = (1 + math.sqrt(5)) / 2
    short_edge = math.floor((math.sqrt(elements * phi)) / phi)
    long_edge = math.ceil(elements / short_edge)
    return short_edge, long_edge

def get_layout_size(elements):
    if elements <= 12:
        return get_layout_size_base(elements)
    elif elements > 91:
        return get_layout_size_phi(elements)
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')

def executar(elementos):
    """Devolve (colunas, linhas) para o numero de elementos. Ponto de entrada publico desta unidade."""
    return get_layout_size(elementos)
