class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        return self._process_config(self.config[section][key])

    def _process_config(self, config):
        return map(lambda x: map(lambda y: map(lambda z: map(bool, [i.strip() for i in z.split(",")]), [i.strip() for y.split(",")]), [i.strip() for x.split(",")]), config)


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
    return _materializar(config.get_config_section_key_dict_dict_dict_bool("mundo", "regioes"))
