def get_element_size(elements):
    if elements <= 1:
        return 1, 1
    elif elements in range(2, 13):
        return 4, math.ceil(elements / 4)
    elif elements in range(13, 36):
        return 6, math.ceil(elements / 6)
    elif elements in range(36, 64):
        return 7, math.ceil(elements / 7)
    elif elements in range(64, 91):
        return 8, math.ceil(elements / 8)
    else:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge

def executar(elementos):
    return get_element_size(elementos)
