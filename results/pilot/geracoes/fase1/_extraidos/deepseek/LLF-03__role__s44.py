import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = self._join_values(value)
        self.logger.info("Config: " + str(self.config))

    def _join_values(self, value):
        return ",".join(map(self._join_values_helper, value))

    def _join_values_helper(self, x):
        return ",".join(map(self._join_values_helper_helper, x))

    def _join_values_helper_helper(self, y):
        return ",".join(map(self._join_values_helper_helper_helper, y))

    def _join_values_helper_helper_helper(self, z):
        return ",".join(z)


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
