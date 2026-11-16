class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        return self._split(self.config[section][key])

    def _split(self, value):
        return list(map(self._split_comma, value.split(",")))

    def _split_comma(self, value):
        return list(map(self._split_dot, value.split(",")))

    def _split_dot(self, value):
        return list(map(self._split_colon, value.split(".")))

    def _split_colon(self, value):
        return list(map(self._split_semicolon, value.split(":")))

    def _split_semicolon(self, value):
        return list(map(self._split_slash, value.split(";")))

    def _split_slash(self, value):
        return list(map(self._split_backslash, value.split("/")))

    def _split_backslash(self, value):
        return list(map(self._split_vertical_bar, value.split("\\")))

    def _split_vertical_bar(self, value):
        return list(map(self._materializar, value.split("|")))

def _materializar(valor):
    """Converte sequencias aninhadas  (inclusive iteradores) em listas."""
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [item for item in itens]


def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(config.get_config_section_key_dict_dict_dict_list("mundo", "regioes"))
