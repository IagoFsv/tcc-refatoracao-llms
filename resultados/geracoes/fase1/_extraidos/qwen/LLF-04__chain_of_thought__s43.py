import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def flatten_list(self, lst):
        return [item for sublist1 in lst for sublist2 in sublist1 for sublist3 in sublist2 for sublist4 in sublist3 for item in sublist4]

    def join_list(self, lst):
        return ",".join(map(str, lst))

    def set_config_dict_dict_dict_dict_int(self, section, key, value):
        flattened_value = self.flatten_list(value)
        joined_value = self.join_list(flattened_value)
        self.config[section][key] = joined_value
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_int("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
