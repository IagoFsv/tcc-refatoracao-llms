class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict(self, section, key):
        def split_by_comma(s):
            return s.split(",")

        def materializar(item):
            if isinstance(item, str):
                return item
            try:
                itens = iter(item)
            except TypeError:
                return item
            return [materializar(item) for item in itens]

        def process_nested_values(value):
            return materializar(value)

        return process_nested_values(
            split_by_comma(
                split_by_comma(
                    split_by_comma(self.config[section][key])
                )
            )
        )


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
    return _materializar(config.get_config_section_key_dict_dict_dict("mundo", "regioes"))
