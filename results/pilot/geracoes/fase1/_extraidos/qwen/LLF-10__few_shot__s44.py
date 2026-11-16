class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        return self._map_nested_strings(self.config[section][key].split(","))

    def _map_nested_strings(self, valor):
        return map(lambda x: map(lambda y: map(lambda z: map(bool, z.split(",")), y.split(",")), x.split(",")), valor)


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
    return _materializar(config.get_config_section_key_dict_dict_dict_bool("mundo", "regioes"))
