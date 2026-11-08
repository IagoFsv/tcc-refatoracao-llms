class Config(object):
    def  __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        return self._map_config(section, key)

    def _map_config(self, section, key):
        return list(map(self._map_config_helper, self.config[section][key].split(",")))

    def _map_config_helper(self, x):
        return list(map(self._map_config_helper_2, x.split(",")))

    def _map_config_helper_2(self, y):
        return list(map(self._map_config_helper_3, y.split(",")))

    def _map_config_helper_3(self, z):
        return list(map(int, z.split(",")))


def _materializar(valor):
    """Converte sequencias aninhadas  (inclusive iteradores) em listas."""
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
