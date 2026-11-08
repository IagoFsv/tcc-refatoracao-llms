class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        return self._process_config(self.config[section][key])

    def _process_config(self, config):
        return map(lambda x: map(lambda y: map(lambda z: map(int, z.split(",")), y.split(",")), x.split(",")), config.split(","))

    def _materializar_valor(self, valor):
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return list(map(self._materializar_valor, itens))

    def executar(self, texto):
        """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return self._materializar_valor(self.config.get_config_section_key_dict_dict_dict_int("mundo", "regioes"))
