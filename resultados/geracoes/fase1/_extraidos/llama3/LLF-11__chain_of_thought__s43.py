class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        valores_aninhados = self.config[section][key].split(",")
        return list(map(self.processar_valor, valores_aninhados))

    def processar_valor(self, valor):
        return list(map(lambda x: list(map(lambda y: list(map(lambda z: z.split(","), y.split(","))), x.split(","))), valor.split(",")))

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
        return list(map(self._materializar, self.get_config_section_key_dict_dict_dict_list("mundo", "regioes")))
