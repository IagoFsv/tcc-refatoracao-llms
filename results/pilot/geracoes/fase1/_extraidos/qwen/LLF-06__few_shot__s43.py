class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        def split_and_map(item, delimiter):
            return map(lambda z: z.split(","), item.split(delimiter))

        texto = self.config[section][key]
        itens_aninhados = split_and_map(texto, ",")
        itens_aninhados = split_and_map(itens_aninhados, ",")
        itens_aninhados = split_and_map(itens_aninhados, ",")
        return itens_aninhados


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
    return _materializar(config.get_config_section_key_dict_dict_list("mundo", "regioes"))
