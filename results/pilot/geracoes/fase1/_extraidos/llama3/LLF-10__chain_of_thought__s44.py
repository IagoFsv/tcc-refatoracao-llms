class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        return processar_valor(self.config[section][key])

    def _materializar(valor):
        # ...

    def executar(texto):
        """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
        config = Config()
        config.config["mundo"] = {"regioes": texto}
        return _materializar(config.get_config_section_key_dict_dict_dict_bool("mundo", "regioes"))
