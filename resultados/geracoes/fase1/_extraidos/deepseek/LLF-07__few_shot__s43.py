class Config(object):
    def  __init__(self):
        self.config  = {}

    def get_config_section_key_dict_dict_dict(self, section, key):
        return map(lambda x: map(lambda y: map(lambda z: z.split(","), y.split(",")), x.split(",")), self.config[section][key].split(","))


def _materializar(valor):
    if isinstance(valor, str):
        return valor
    try:
        itens  = iter(valor)
    except TypeError:
        return valor
    return [ _materializar(item) for item in itens]


def executar(texto):
    config  = Config()
    config.config["mundo"]  = {"regioes": texto}
    return _materializar(config.get_config_section_key_dict_dict_dict("mundo", "regioes"))


def split_values(value):
    return value.split(",")


def split_sections(config, section, key):
    return map(split_values, config[section][key].split(","))


def get_config_section_key_dict_dict_dict(config, section, key):
    return _materializar(split_sections(config, section, key))


def executar(texto):
    config  = Config()
    config.config["mundo"]  = {"regioes": texto}
    return get_config_section_key_dict_dict_dict(config.config, "mundo", "regioes")
