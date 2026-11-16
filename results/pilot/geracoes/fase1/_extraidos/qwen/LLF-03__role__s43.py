import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = self._join_value(value)
        self.logger.info("Config: " + str(self.config))

    def _join_value(self, value):
        return ",".join(map(self._join_layer, value))

    def _join_layer(self, layer):
        return ",".join(map(self._join_layer, layer))

    def _join_layer(self, layer):
        return ",".join(layer)


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
