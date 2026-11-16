class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        config_section = self.config.get(section, {})
        config_key = config_section.get(key, [])
        return list(map(self._convert_float, map(self._split, config_key)))

    def _split(self, item):
        return list(map(lambda z: z.split(','), item.split(',')))

    def _convert_float(self, item):
        return float(item)

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
        return self._materializar(self.config.get_config_section_key_dict_dict_dict_float("mundo", "regioes"))
