class Config(object):
    def __init__(self):
        self.config = {}

    def process_config_value(self, x):
        return [list(map(lambda z: z.split(","), y.split(","))) for y in x.split(",")]

    def get_config_section_key_dict_dict_dict(self, section, key):
        return map(lambda x: map(lambda y: self.process_config_value(y), x.split(",")), self.config[section][key].split(","))

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
        config = Config()
        config.config["mundo"] = {"regioes": texto}
        return _materializar(config.get_config_section_key_dict_dict_dict("mundo", "regioes"))
