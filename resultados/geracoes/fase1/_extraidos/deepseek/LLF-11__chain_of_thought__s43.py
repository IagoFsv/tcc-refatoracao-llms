class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        return self.map_values(self.config[section][key])

    def map_values(self, value):
        return self.split_and_map(value, ",")

    def split_and_map(self, value, split_char):
        return list(map(lambda x: self.split_and_map(x, split_char), value.split(split_char)))


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
    return _materializar(config.get_config_section_key_dict_dict_dict_list("mundo", "regioes"))
