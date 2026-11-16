class Config(object):
    def __init__(self):
        self.config = {}

    def parse_config_value(self, value):
        """Parses a comma-separated string into a nested list of integers."""
        return map(self.parse_level3, value.split(","))

    def parse_level3(self, value):
        """Parses a comma-separated string into a list of integers."""
        return map(self.parse_level2, value.split(","))

    def parse_level2(self, value):
        """Parses a comma-separated string into a list of integers."""
        return map(int, value.split(","))

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        return self.parse_config_value(self.config[section][key])


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
