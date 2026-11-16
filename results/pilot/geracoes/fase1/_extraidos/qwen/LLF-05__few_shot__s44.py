import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_values(self, value):
        return ",".join(map(str, value))

    def join_values_list(self, value):
        return ",".join(map(self.join_values, value))

    def join_values_list_list(self, value):
        return ",".join(map(self.join_values_list, value))

    def join_values_list_list_list(self, value):
        return ",".join(map(self.join_values_list_list, value))

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = self.join_values_list_list_list(value)
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
