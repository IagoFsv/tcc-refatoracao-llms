class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict(self, section, key):
        return self._map_third_level(self._map_second_level(self._map_first_level(self.config[section][key].split(","))))

    def _map_first_level(self, value):
        return map(self._split_by_comma, value)

    def _map_second_level(self, value):
        return map(self._map_first_level, value)

    def _map_third_level(self, value):
        return map(self._map_second_level, value)

    def _split_by_comma(self, value):
        return value.split(",")


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
    return _materializar(config.get_config_section_key_dict_dict_dict("mundo", "regioes"))
