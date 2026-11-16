import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_nested_values(self, nested_values):
        return ",".join(map(self.join_nested_values, nested_values)) if isinstance(nested_values, list) else nested_values

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = self.join_nested_values(value)
        self.logger.info("Config: " + str(self.config))

def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
