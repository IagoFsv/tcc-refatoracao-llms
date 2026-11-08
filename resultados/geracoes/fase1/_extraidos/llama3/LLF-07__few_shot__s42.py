class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict(self, section, key):
        config_section = self.config[section][key]
        return list(map(lambda x: list(map(lambda y: list(map(lambda z: z.split(","), y.split(","))), x.split(","))), config_section.split(",")))

    def _materializar(self, valor):
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return list(map(self._materializar, itens))

    def executar(self, texto):
        self.config["mundo"] = {"regioes": texto}
        return self._materializar(self.get_config_section_key_dict_dict("mundo", "regioes"))
