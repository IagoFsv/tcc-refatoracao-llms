class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        return self._split_and_map(self.config[section][key], 3)

    def _split_and_map(self, value, levels):
        return map(lambda x: self._split_and_map(x, levels - 1), value.split(",")) if levels > 1 else value.split(",")


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
    return _materializar(config.get_config_section_key_dict_dict_list("mundo", "regioes"))
