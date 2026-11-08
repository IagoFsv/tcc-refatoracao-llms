import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def _join_str(self, value):
        return ",".join(map(str, value))

    def _join_level3(self, z):
        return ",".join(map(self._join_str, z))

    def _join_level2(self, y):
        return ",".join(map(self._join_level3, y))

    def _join_level1(self, x):
        return ",".join(map(self._join_level2, x))

    def set_config_dict_dict_dict_dict_int(self, section, key, value):
        self.config[section][key] = self._join_level1(value)
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_int("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
