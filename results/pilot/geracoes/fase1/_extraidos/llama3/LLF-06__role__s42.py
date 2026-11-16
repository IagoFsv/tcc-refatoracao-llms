class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        def get_value(x):
            return list(map(lambda y: list(map(lambda z: z.split(','), y.split(','))), x.split(',')))
        return list(map(get_value, self.config[section][key].split(',')))

    def materializar(self, valor):
        """Converte sequencias aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return [self.materializar(item) for item in itens]

    def executar(self, texto):
        """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return self.materializar(self.get_config_section_key_dict_dict_list("mundo", "regioes"))
