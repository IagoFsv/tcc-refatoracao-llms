class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        def extract_values(x):
            return [item.split(',') for item in x.split(',')]
        return list(map(lambda y: map(lambda z: map(lambda w: w.split(','), z.split(',')), y.split(',')), map(extract_values, self.config[section][key].split(','))))

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
        config = self
        config.config["mundo"] = {"regioes": texto}
        return config.materializar(config.get_config_section_key_dict_dict_dict_list("mundo", "regioes"))
