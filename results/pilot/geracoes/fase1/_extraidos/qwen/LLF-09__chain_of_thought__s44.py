class Config(object):
    def __init__(self):
        self.config = {}

    def split_and_convert_to_float(self, value):
        """Splits the value by commas and converts each part to float."""
        return map(float, value.split(","))

    def split_and_convert_to_list(self, value):
        """Splits the value by commas and converts each part to a list of floats."""
        return map(self.split_and_convert_to_float, value.split(","))

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return self.split_and_convert_to_list(self.config[section][key])


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
