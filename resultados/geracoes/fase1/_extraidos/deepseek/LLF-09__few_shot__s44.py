class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return map(lambda x: map(lambda y: map(lambda z: map(float, z.split(",")), y.split(",")), x.split(",")), self.config[section][key].split(","))


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
    return _materializar(config.get_config_section_key_dict_dict_dict_float("mundo", "regioes"))


def _split_and_convert(value):
    return map(float, value.split(","))


def _materializar_config(config):
    return map(lambda x: map(lambda y: map(lambda z: map(_split_and_convert, z), y.split(",")), x.split(",")), config.split(","))


executar("1,2,3,4,5")
