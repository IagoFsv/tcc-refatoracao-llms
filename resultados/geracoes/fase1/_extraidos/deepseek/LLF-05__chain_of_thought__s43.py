import logging


class Config(object):
    def  __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def convert_values_to_string(self, value):
        return ",".join(map(self.convert_values_to_string, value)) if isinstance(value, list) else str(value)

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = self.convert_values_to_string(value)
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
