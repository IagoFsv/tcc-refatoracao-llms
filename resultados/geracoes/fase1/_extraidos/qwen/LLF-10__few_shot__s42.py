class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        return self._process_config_value(self.config[section][key])

    def _process_config_value(self, value):
        return map(self._split_and_convert, value.split(","))

    def _split_and_convert(self, item):
        return map(bool, item.split(","))


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
