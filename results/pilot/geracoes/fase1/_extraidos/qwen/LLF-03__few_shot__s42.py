import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_values(self, value):
        return ",".join(value)

    def join_values_nested(self, value):
        return ",".join(map(self.join_values, value))

    def join_values_nested_multiple(self, value):
        return ",".join(map(self.join_values_nested, value))

    def join_values_nested_multiple_multiple(self, value):
        return ",".join(map(self.join_values_nested_multiple, value))

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = self.join_values_nested_multiple_multiple(value)
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
