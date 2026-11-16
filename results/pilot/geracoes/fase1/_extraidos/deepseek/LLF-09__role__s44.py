class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return self.map_values(self.config[section][key], self.map_values, self.map_values, self.map_values, self.map_values, self.float_split)

    @staticmethod
    def map_values(value, map_func):
        return map(map_func, value.split(","))

    @staticmethod
    def float_split(value):
        return map(float, value.split(","))


def _materializar(valor):
    """Converte sequencias aninhadas  (inclusive iteradores) em listas."""
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
