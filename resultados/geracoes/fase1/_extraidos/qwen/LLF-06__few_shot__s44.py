class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        return self._split_and_map(self.config[section][key], 3)

    def _split_and_map(self, value, levels):
        for _ in range(levels):
            value = map(lambda x: map(lambda y: y.split(","), x.split(",")), value.split(","))
        return value


def _materializar(valor):
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [_materializar(item) for item in itens]


def executar(texto):
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(config.get_config_section_key_dict_dict_list("mundo", "regioes"))
