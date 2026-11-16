class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        def get_value(x):
            return list(map(int, x.split(",")))
        return list(map(lambda y: list(map(get_value, y.split(","))), list(map(get_value, x.split(",")))) for x in self.config[section][key].split(","))

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
        return self.materializar(list(map(lambda x: list(map(int, x.split(","))), self.get_config_section_key_dict_dict_dict_int("mundo", "regioes").__next__())))
