class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict(self, section, key):
        def split_and_map(input_str):
            return map(lambda x: map(lambda y: map(lambda z: z.split(","), y.split(",")), x.split(",")), input_str.split(","))

        return split_and_map(self.config[section][key])


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
    return _materializar(config.get_config_section_key_dict_dict_dict("mundo", "regioes"))
