class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict(self, section, key):
        def process_element(element):
            return [x.split(',') for x in element.split(',')]
        return map(lambda x: map(process_element, x.split(',')), self.config[section][key].split(','))

    def materializar(self, valor):
        """Converte sequências aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return [_materializar(item) for item in itens]

    def executar(self, texto):
        """Le o texto gravado na configuração, como listas. Ponto de entrada público desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return self.materializar(self.get_config_section_key_dict_dict_dict("mundo", "regioes"))
