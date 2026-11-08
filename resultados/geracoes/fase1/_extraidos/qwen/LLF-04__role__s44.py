import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_int(self, section, key, value):
        self.config[section][key] = ",".join(self._join_values(value))
        self.logger.info("Config: " + str(self.config))

    def _join_values(self, value):
        return ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(map(str, z)), y)), x)), value))

def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_int("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
