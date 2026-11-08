class Config(object):
    def  __init__(self):
        self.config  = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        return self.map_values(self.config[section][key])

    def map_values(self, value):
        return list(map(self.map_values, value.split(",")))


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
    return _materializar(config.get_config_section_key_dict_dict_dict_list("mundo", "regioes"))
