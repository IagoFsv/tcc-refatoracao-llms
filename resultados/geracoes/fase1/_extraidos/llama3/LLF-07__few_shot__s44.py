class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict(self, section, key):
        return self._parse_config_value(self.config[section][key])

    def _parse_config_value(self, value):
        return map(self._parse_config_item, value.split(","))

    def _parse_config_item(self, item):
        return self._materializar(item.split(","))

    def _materializar(self, valor):
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
    return _materializar(config.get_config_section_key_dict_dict("mundo", "regioes"))
