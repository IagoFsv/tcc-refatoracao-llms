class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        def split_by_comma(value):
            return value.split(",")

        def materializar(valor):
            """Converte sequencias aninhadas (inclusive iteradores) em listas."""
            if isinstance(valor, str):
                return valor
            try:
                itens = iter(valor)
            except TypeError:
                return valor
            return [materializar(item) for item in itens]

        def process_section_key(section, key):
            return materializar(
                map(split_by_comma, split_by_comma(self.config[section][key]))
            )

        return process_section_key(section, key)


def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return config.get_config_section_key_dict_dict_list("mundo", "regioes")
