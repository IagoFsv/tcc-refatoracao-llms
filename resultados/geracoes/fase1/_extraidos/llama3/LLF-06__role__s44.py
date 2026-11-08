class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        config_value = self.config[section][key]
        return list(map(self._process_config_value, config_value.split(",")))

    def _process_config_value(self, value):
        return list(map(self._materializar, value.split(",")))

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
