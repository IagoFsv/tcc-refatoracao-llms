import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def flatten_list(self, nested_list):
        return [item for sublist in nested_list for subsublist in sublist for item in subsublist]

    def join_values(self, values):
        return ",".join(map(str, values))

    def set_config_dict_dict_dict_list(self, section, key, value):
        flattened = self.flatten_list(value)
        joined = self.join_values(flattened)
        self.config[section][key] = joined
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
