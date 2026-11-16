class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        def convert_to_float(group):
            return list(map(float, group.split(",")))
        return list(map(lambda x: list(map(convert_to_float, x.split(","))), self.config[section][key].split(",")))

    def materializar(self, valor):
        """Converte sequencias aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return list(map(self.materializar, itens))

    def executar(self, texto):
        """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return self.materializar(self.get_config_section_key_dict_dict_dict_float("mundo", "regioes"))
