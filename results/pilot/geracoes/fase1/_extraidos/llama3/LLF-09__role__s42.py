class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return self._process_config(self.config[section][key])

    def _process_config(self, config):
        return map(lambda x: map(lambda y: map(lambda z: list(map(float, z.split(",")))), y.split(",")), x.split(","))

    def _materializar_valor(self, valor):
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return [self._materializar_valor(item) for item in itens]

    def _materializar(self, valor):
        if isinstance(valor, list):
            return [self._materializar_valor(item) for item in valor]
        return self._materializar_valor(valor)

    def executar(self, texto):
        """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
        config = self
        config.config["mundo"] = {"regioes": texto}
        return self._materializar(config.get_config_section_key_dict_dict_dict_float("mundo", "regioes"))
