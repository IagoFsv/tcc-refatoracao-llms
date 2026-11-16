import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_values(self, value):
        return ",".join(value)

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = self.join_values(self.join_values(self.join_values(value)))
        self.logger.info("Config: " + str(self.config))

def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
