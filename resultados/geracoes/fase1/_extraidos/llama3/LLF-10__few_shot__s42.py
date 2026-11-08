class Config(object):
    def __init__(self):
        self.config = {}

    def _get_config_section_key_dict_dict_dict_bool(self, section, key):
        return self._map_to_bool(self.config[section][key].split(","))

    def _map_to_bool(self, values):
        return map(lambda x: map(lambda y: map(bool, y.split(",")), x.split(",")), values)

    def _materializar(valor):
        """Converte sequencias aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return [_materializar(item) for item in itens]

    def executar(self, texto):
        """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return _materializar(self._get_config_section_key_dict_dict_dict_bool("mundo", "regioes"))
