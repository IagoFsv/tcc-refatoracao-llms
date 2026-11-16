import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = self._join_values(value)
        self.logger.info("Config: " + str(self.config))

    def _join_values(self, value):
        return ",".join(map(self._join_values_inner, value))

    def _join_values_inner(self, value):
        return ",".join(map(self._join_values_inner_inner, value))

    def _join_values_inner_inner(self, value):
        return ",".join(map(self._join_values_inner_inner_inner, value))

    def _join_values_inner_inner_inner(self, value):
        return ",".join(map(str, value))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
