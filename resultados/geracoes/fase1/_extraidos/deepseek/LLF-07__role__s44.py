class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict(self, section, key):
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
    return _materializar(config.get_config_section_key_dict_dict_dict("mundo", "regioes"))


def split_comma_separated(value):
    return value.split(",")


def map_split_comma_separated(function, value):
    return map(function, value.split(","))


def map_map_split_comma_separated(function, value):
    return map(lambda x: map_split_comma_separated(function, x), value.split(","))


def map_map_map_split_comma_separated(function, value):
    return map(lambda x: map(lambda y: map_split_comma_separated(function, y), x.split(",")), value.split(","))


def get_config_section_key_dict_dict_dict(config, section, key):
    return map_map_map_split_comma_separated(split_comma_separated, config[section][key])


def executar_refactored(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(get_config_section_key_dict_dict_dict(config.config, "mundo", "regioes"))
