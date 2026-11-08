class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        return list(map(lambda x: list(map(lambda y: list(map(lambda z: list(map(bool, z.split(","))), y.split(","))), x.split(","))), self.config[section][key].split(",")))


def _materializar(valor):
    """Converte sequencias aninhadas (inclusive iteradores) em listas."""
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [_materializar(item) for item in itens]


def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(config.get_config_section_key_dict_dict_dict_bool("mundo", "regioes"))
