import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_values(self, values):
        return ",".join(values)

    def join_values_multiple(self, values):
        return ",".join(map(self.join_values, values))

    def join_values_multiple_multiple(self, values):
        return ",".join(map(self.join_values_multiple, values))

    def join_values_multiple_multiple_multiple(self, values):
        return ",".join(map(self.join_values_multiple_multiple, values))

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = self.join_values_multiple_multiple_multiple(value)
        self.logger.info("Config: " + str(self.config))

def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
