import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def _join_values(self, z):
        return ",".join(z)

    def _join_y(self, y):
        return ",".join(map(self._join_values, y))

    def _join_x(self, x):
        return ",".join(map(self._join_y, x))

    def _join_section(self, section):
        return ",".join(map(self._join_x, section))

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = self._join_section(value)
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
