class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return self._split_and_convert(self.config[section][key], float)

    def _split_and_convert(self, value, converter):
        return map(converter, value.split(","))

    def _split_and_convert_list(self, value, converter):
        return map(lambda x: self._split_and_convert(x, converter), value.split(","))

    def _split_and_convert_dict(self, value, converter):
        return map(lambda x: self._split_and_convert_list(x, converter), value.split(","))

    def _split_and_convert_dict_dict(self, value, converter):
        return map(lambda x: self._split_and_convert_dict(x, converter), value.split(","))


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
    return _materializar(config.get_config_section_key_dict_dict_dict_float("mundo", "regioes"))
