class Config(object):
    def __init__(self):
        self.config = {}

    def split_and_convert_to_bool(self, value):
        return map(bool, value.split(","))

    def split_and_convert_to_list(self, value):
        return map(self.split_and_convert_to_bool, value.split(","))

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        return map(self.split_and_convert_to_list, self.config[section][key].split(","))


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
