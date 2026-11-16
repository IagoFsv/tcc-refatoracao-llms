class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        config_section = self.config.get(section, {})
        config_key = config_section.get(key, [])
        return list(map(self._convert_to_int, config_key))

    def _convert_to_int(self, value):
        return list(map(int, value.split(",")))

    def _materializar(self, valor):
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
        return self._materializar(self.get_config_section_key_dict_dict_dict_int("mundo", "regioes"))
