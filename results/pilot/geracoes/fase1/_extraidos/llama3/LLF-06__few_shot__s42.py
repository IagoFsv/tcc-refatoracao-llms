class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        def get_key_value(x):
            return list(map(lambda y: list(map(lambda z: z.split(","), y.split(","))), x.split(",")))

        return list(map(get_key_value, self.config[section][key].split(",")))

    def _materializar(self, valor):
        """Converte sequencias aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return list(map(self._materializar, itens))


def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return config._materializar(config.get_config_section_key_dict_dict_list("mundo", "regioes"))
