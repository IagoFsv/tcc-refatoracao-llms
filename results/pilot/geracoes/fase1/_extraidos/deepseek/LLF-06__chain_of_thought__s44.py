class Config(object):
    def  __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        return self.map_values(self.config[section][key])

    def map_values(self, value):
        return self.split_and_map(value, ',', self.split_and_map, ',')

    def split_and_map(self, value, splitter, func, joiner):
        return [func(item, splitter, func, joiner) if splitter in item else item for item in value.split(splitter)]

def _materializar(valor):
    """Converte sequencias aninhadas  (inclusive iteradores) em listas."""
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [ _materializar(item) for item in itens]


def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(config.get_config_section_key_dict_dict_list("mundo", "regioes"))
