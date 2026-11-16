class Config(object):
    def __init__(self):
        self.config = {}

    def _get_config_section_key_dict_dict_dict(self, section, key):
        return [
            [
                [list(map(bool, z.split(","))) for z in y.split(",")] for y in x.split(",")
            ] for x in self.config[section][key].split(",")
        ]

    def _materializar(self, valor):
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return [_materializar(item) for item in itens]

    def executar(self, texto):
        self.config["mundo"] = {"regioes": texto}
        return self._materializar(self._get_config_section_key_dict_dict_dict("mundo", "regioes"))
