class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        valores_aninhados = self.config[section][key].split(",")
        return list(map(lambda x: list(map(lambda y: list(map(lambda z: bool(z), y.split(","))), x.split(","))), valores_aninhados))

    def processar_valor(self, valor):
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return list(map(self.processar_valor, itens))

    def executar(self, texto):
        """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
        self.config["mundo"] = {"regioes": texto}
        return self.processar_valor(self.get_config_section_key_dict_dict_dict_bool("mundo", "regioes"))
