class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        return map(lambda x: map(lambda y: map(lambda z: map(int, z.split(",")), y.split(",")), x.split(",")), self.config[section][key].split(","))


def _materializar(valor):
    """Converte sequencias aninhadas (inclusive iteradores) em listas."""
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
    return _materializar(config.get_config_section_key_dict_dict_dict_int("mundo", "regioes"))


def string_to_int_list(valor):
    """Converte uma string separada por vírgulas em uma lista de inteiros."""
    return map(int, valor.split(","))


def split_and_materialize(valor):
    """Divide uma string em partes e a converte em uma lista."""
    return map(_materializar, valor.split(","))


def get_config_section_key_dict_dict_dict_int(config, section, key):
    """Obtém uma configuração específica da seção e chave, convertendo os valores para int."""
    return map(lambda x: map(lambda y: map(lambda z: map(string_to_int_list, z), y), x), split_and_materialize(config[section][key]))


def executar_refatorado(texto):
    """Le o texto gravado na configuração, como listas. Ponto de entrada público desta unidade refatorada."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(get_config_section_key_dict_dict_dict_int(config.config, "mundo", "regioes"))
