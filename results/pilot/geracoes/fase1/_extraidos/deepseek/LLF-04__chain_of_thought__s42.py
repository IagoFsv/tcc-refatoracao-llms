import logging


class Config(object):
    def  __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_int(self, section, key, value):
        self.config[section][key] = self.convert_to_string(value)
        self.logger.info("Config: " + str(self.config))

    def convert_to_string(self, value):
        return ",".join(map(self.convert_inner_to_string, value))

    def convert_inner_to_string(self, value):
        return ",".join(map(self.convert_middle_to_string, value))

    def convert_middle_to_string(self, value):
        return ",".join(map(self.convert_outer_to_string, value))

    def convert_outer_to_string(self, value):
        return ",".join(map(str, value))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_int("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
