class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        return self._process_config(self.config[section][key])

    def _process_config(self, config):
        return map(lambda x: map(lambda y: map(lambda z: map(lambda w: w.split(","), z.split(",")), y.split(",")), x.split(",")), config)

    def _materializar(self, valor):
        """Converte sequencias aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return [_materializar(item) for item in itens]

    def executar(self, texto):
        """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return self._materializar(self.get_config_section_key_dict_dict_dict_list("mundo", "regioes"))
