class Config(object):
    def __init__(self):
        self.config = {}

    def process_section_key_dict_dict_dict(self, section, key):
        result = []
        for x in self.config[section][key].split(","):
            result.append([list(map(int, z.split(","))) for z in x.split(",")])
        return result

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        return self.process_section_key_dict_dict_dict(section, key)


def _materializar(valor):
    """Converte sequencias aninhadas (inclusive iteradores) em listas."""
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [_materializar(item) for item in itens]


def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(config.get_config_section_key_dict_dict_dict_int("mundo", "regioes"))
