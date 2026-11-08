import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = self.convert_values(value)
        self.logger.info("Config: " + str(self.config))

    def convert_values(self, value):
        return ",".join(map(self.convert_values_inner, value))

    def convert_values_inner(self, value):
        return ",".join(map(self.convert_values_middle, value))

    def convert_values_middle(self, value):
        return ",".join(map(self.convert_values_outer, value))

    def convert_values_outer(self, value):
        return ",".join(map(str, value))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
