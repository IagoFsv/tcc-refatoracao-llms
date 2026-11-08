import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def flatten_list(self, lst):
        return [item for sublist in lst for item in sublist]

    def flatten_list_of_lists(self, lst):
        return [item for sublist in sublist for item in sublist]

    def flatten_list_of_lists_of_lists(self, lst):
        return [item for sublist in sublist for sublist2 in sublist for item in sublist2]

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        flattened_value = self.flatten_list_of_lists_of_lists(value)
        joined_value = ",".join(map(str, flattened_value))
        self.config[section][key] = joined_value
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
