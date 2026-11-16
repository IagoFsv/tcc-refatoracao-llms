class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        return map(lambda x: map(lambda y: map(lambda z: z.split(","), y.split(",")), x.split(",")), self.config[section][key].split(","))


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
    return _materializar(config.get_config_section_key_dict_dict_list("mundo", "regioes"))


def split_and_strip(value):
    return [item.strip() for item in value.split(",")]


def map_split_and_strip(value):
    return map(split_and_strip, value)


def map_map_split_and_strip(value):
    return map(lambda x: map(split_and_strip, x), value)


def get_config_section_key_dict_dict_list(config, section, key):
    return map_map_split_and_strip(config[section][key].split(","))


def executar_refatorado(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(get_config_section_key_dict_dict_list(config.config, "mundo", "regioes"))
