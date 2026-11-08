class Config(object):
    def __init__(self):
        self.config = {}

    def _get_config_section_key_dict_dict_dict(self, section, key):
        return [
            [
                [
                    [list(map(str.split, item.split(","))) for item in items.split(",")]
                    for items in section_items.split(",")
                ]
                for section_items in self.config[section][key].split(",")
            ]
            for section in self.config
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
        return _materializar(self._get_config_section_key_dict_dict_dict("mundo", "regioes"))
