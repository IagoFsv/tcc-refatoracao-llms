import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self._transform_values(value)
        self.config[section][key] = value
        self.logger.info("Config: " + str(self.config))

    def _transform_values(self, value):
        value = self._transform_4_dimensions(value)
        return value

    def _transform_4_dimensions(self, value):
        return ",".join(map(self._transform_3_dimensions, value))

    def _transform_3_dimensions(self, value):
        return ",".join(map(self._transform_2_dimensions, value))

    def _transform_2_dimensions(self, value):
        return ",".join(map(self._transform_1_dimension, value))

    def _transform_1_dimension(self, value):
        return ",".join(map(str, value))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
