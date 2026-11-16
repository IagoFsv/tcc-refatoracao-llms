"""Leitura de valores aninhados da configuracao do jogo, gravados como texto.

Ponto de entrada publico: executar(texto). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return map(lambda x: map(lambda y: map(lambda z: map(float, z.split(",")), y.split(",")), x.split(",")), self.config[section][key].split(","))


def _materializar(valor):
    """Converte sequencias aninhadas  (inclusive iteradores) em listas."""
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [ _materializar(item) for item in itens]


def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(config.get_config_section_key_dict_dict_dict_float("mundo", "regioes"))


def convert_to_float(value):
    """Converte uma string numérica em float."""
    return float(value)


def split_string(value, delimiter):
    """Divide uma string em uma lista de substrings."""
    return value.split(delimiter)


def map_function(function, iterable):
    """Aplica uma função a cada item de um iterável."""
    return map(function, iterable)


def map_to_floats(iterable):
    """Converte cada item de um iterável em float."""
    return map_function(convert_to_float, iterable)


def map_to_strings(iterable, delimiter):
    """Divide cada item de um iterável em uma lista de substrings."""
    return map_function(lambda x: split_string(x, delimiter), iterable)


def map_to_lists(iterable, delimiter):
    """Converte cada item de um iterável em uma lista."""
    return map_function(lambda x: _materializar(map_to_floats(map_to_strings(x, delimiter))), iterable)


def executar_refatorado(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return map_to_lists(split_string(config.config["mundo"]["regioes"], ","), ",")
