import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_values(self, value):
        return ",".join(value)

    def join_sub_values(self, value):
        return ",".join(map(self.join_values, value))

    def join_sub_sub_values(self, value):
        return ",".join(map(self.join_sub_values, value))

    def join_sub_sub_sub_values(self, value):
        return ",".join(map(self.join_sub_sub_values, value))

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = self.join_sub_sub_sub_values(value)
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
