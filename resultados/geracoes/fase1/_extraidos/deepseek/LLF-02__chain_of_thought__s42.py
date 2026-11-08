import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = self.join_values(value)
        self.logger.info("Config: " + str(self.config))

    def join_values(self, value):
        return ",".join(self.map_values(value))

    def map_values(self, value):
        return list(map(self.inner_map, value))

    def inner_map(self, value):
        return list(map(self.middle_map, value))

    def middle_map(self, value):
        return list(map(self.outer_map, value))

    def outer_map(self, value):
        return ",".join(value)


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
