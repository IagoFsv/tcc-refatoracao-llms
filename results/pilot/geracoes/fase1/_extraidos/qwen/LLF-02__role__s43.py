import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = self._join_list(value)
        self.logger.info("Config: " + str(self.config))

    def _join_list(self, value):
        return ",".join(map(self._join_tuple, value))

    def _join_tuple(self, value):
        return ",".join(map(self._join_pair, value))

    def _join_pair(self, value):
        return ",".join(map(self._join_element, value))

    def _join_element(self, value):
        return ",".join(value)


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
