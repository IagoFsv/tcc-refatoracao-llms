class Config(object):
    def __init__(self):
        self.config = {}

    def _get_config_section_key_dict(self, section, key):
        return self.config[section][key]

    def _map_to_int(self, values):
        return map(lambda x: map(int, x.split(",")), values)

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        values = self._get_config_section_key_dict(section, key)
        return list(map(lambda x: list(map(int, x.split(","))), values.split(",")))

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
        return _materializar(config.get_config_section_key_dict_dict_dict_int("mundo", "regioes"))
