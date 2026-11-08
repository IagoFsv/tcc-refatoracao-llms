class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict(self, section, key):
        config = self.config[section][key].split(",")
        return self._map_split_values(config)

    def _map_split_values(self, values):
        return list(map(lambda x: list(map(lambda y: list(map(lambda z: z.split(","), y.split(","))), x.split(","))), values))

    def _materializar(self, valor):
        """Converte sequencias aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return list(map(self._materializar, itens))

    def executar(self, texto):
        """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return self._materializar(self.config["mundo"]["regioes"])
