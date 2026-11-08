class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        return self._split_and_map(self.config[section][key], 4)

    def _split_and_map(self, valor, n):
        for _ in range(n):
            valor = map(lambda x: map(lambda y: map(lambda z: map(lambda w: w.split(","), z.split(",")), y.split(",")), x.split(",")), valor.split(","))
        return valor


def _materializar(valor):
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [_materializar(item) for item in itens]


def executar(texto):
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(config.get_config_section_key_dict_dict_dict_list("mundo", "regioes"))
