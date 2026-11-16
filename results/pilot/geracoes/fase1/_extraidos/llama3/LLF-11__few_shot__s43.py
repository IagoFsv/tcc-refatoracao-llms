class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        def _map_values(values):
            return list(map(lambda x: list(map(lambda y: list(map(lambda z: list(map(lambda w: w.split(','), z.split(','))), y.split(','))), x.split(','))), values.split(',')))

        return _map_values(self.config[section][key])

    def _materializar(valor):
        """Converte sequências aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return list(map(_materializar, itens))

    def executar(self, texto):
        """Le o texto gravado na configuração, como listas. Ponto de entrada público desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return _materializar(self.get_config_section_key_dict_dict_dict_list("mundo", "regioes"))
