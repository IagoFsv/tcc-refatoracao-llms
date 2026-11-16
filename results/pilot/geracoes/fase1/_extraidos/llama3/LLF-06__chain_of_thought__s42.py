class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section(self, section):
        return self.config.get(section, {})

    def get_config_key_dict(self, section, key):
        return self.get_config_section(section)[key]

    def get_config_key_dict_dict_list(self, section, key):
        return [list(map(lambda x: x.split(','), y.split(','))) for y in self.get_config_key_dict(section, key).split(',')]

    def _materializar(self, valor):
        """Converte sequências aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return [_materializar(item) for item in itens]

    def executar(self, texto):
        """Le o texto gravado na configuração, como listas. Ponto de entrada público desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return self._materializar(self.get_config_key_dict_dict_list("mundo", "regioes"))
