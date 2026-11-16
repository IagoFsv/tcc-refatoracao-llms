class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict(self, section, key):
        return self.config[section][key].split(",")

    def get_config_section_key_dict_dict(self, section, key):
        return list(map(lambda x: self._process_line(x), self.get_config_section_key_dict(section, key)))

    def _process_line(self, line):
        return list(map(lambda x: x.split(","), line.split(",")))

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
        return self._materializar(self.get_config_section_key_dict_dict("mundo", "regioes"))
