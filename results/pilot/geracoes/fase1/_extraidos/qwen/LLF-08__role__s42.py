class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        return self._parse_nested_values(self.config[section][key].split(","))

    def _parse_nested_values(self, values):
        return map(self._parse_value, values)

    def _parse_value(self, value):
        return map(self._parse_value, value.split(","))

    def _parse_int(self, value):
        return map(int, value.split(","))


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
    return _materializar(config.get_config_section_key_dict_dict_dict_int("mundo", "regioes"))
