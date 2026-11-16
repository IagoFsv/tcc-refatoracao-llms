import math

def get_layout_size(elements):
    if elements <= 1:
        return 1, 1
    elif elements <= 12:
        return get_layout_size_for_small_elements(elements)
    elif elements <= 18:
        return get_layout_size_for_elements_13_to_18(elements)
    elif elements <= 24:
        return get_layout_size_for_elements_19_to_24(elements)
    elif elements <= 30:
        return get_layout_size_for_elements_25_to_30(elements)
    elif elements <= 35:
        return get_layout_size_for_elements_31_to_35(elements)
    elif elements <= 42:
        return get_layout_size_for_elements_36_to_42(elements)
    elif elements <= 49:
        return get_layout_size_for_elements_43_to_49(elements)
    elif elements <= 56:
        return get_layout_size_for_elements_50_to_56(elements)
    elif elements <= 63:
        return get_layout_size_for_elements_57_to_63(elements)
    elif elements <= 70:
        return get_layout_size_for_elements_64_to_70(elements)
    elif elements <= 77:
        return get_layout_size_for_elements_71_to_77(elements)
    elif elements <= 84:
        return get_layout_size_for_elements_78_to_84(elements)
    elif elements <= 91:
        return get_layout_size_for_elements_85_to_91(elements)
    elif elements > 91:
        phi = (1 + math.sqrt(5)) / 2
        short_edge = math.floor((math.sqrt(elements * phi)) / phi)
        long_edge = math.ceil(elements / short_edge)
        return short_edge, long_edge
    else:
        raise ValueError(f'Unsupported number of elements: {elements}')


def get_layout_size_for_small_elements(elements):
    return elements, 1


def get_layout_size_for_elements_13_to_18(elements):
    return elements // 3, 3


def get_layout_size_for_elements_19_to_24(elements):
    return elements // 4, 4


def get_layout_size_for_elements_25_to_30(elements):
    return elements // 5, 5


def get_layout_size_for_elements_31_to_35(elements):
    return elements // 6, 6


def get_layout_size_for_elements_36_to_42(elements):
    return 7, 6


def get_layout_size_for_elements_43_to_49(elements):
    return 7, 7


def get_layout_size_for_elements_50_to_56(elements):
    return 7, 8


def get_layout_size_for_elements_57_to_63(elements):
    return 7, 9


def get_layout_size_for_elements_64_to_70(elements):
    return 7, 10


def get_layout_size_for_elements_71_to_77(elements):
    return 7, 11


def get_layout_size_for_elements_78_to_84(elements):
    return 7, 12


def get_layout_size_for_elements_85_to_91(elements):
    return 7, 13


def executar(elementos):
    """Devolve (colunas, linhas) para o numero de elementos. Ponto de entrada publico desta unidade."""
    return get_layout_size(elementos)
