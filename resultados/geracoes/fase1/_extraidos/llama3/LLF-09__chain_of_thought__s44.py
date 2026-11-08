class Config(object):
    def __init__(self):
        self.config = {}

    def parse_config_value(self, x):
        return [map(float, z.split(",")) for z in map(lambda y: y.split(","), x.split(","))]

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return map(self.parse_config_value, self.config[section][key].split(","))

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
        config = Config()
        config.config["mundo"] = {"regioes": texto}
        return _materializar(config.get_config_section_key_dict_dict_dict_float("mundo", "regioes"))
