import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_values(self, values):
        return ",".join(map(str, values))

    def join_lists(self, lists):
        return ",".join(map(self.join_values, lists))

    def join_dicts(self, dicts):
        return ",".join(map(self.join_lists, dicts))

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = self.join_dicts(value)
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
