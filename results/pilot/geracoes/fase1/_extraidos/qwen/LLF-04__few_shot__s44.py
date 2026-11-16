import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def join_values(self, value):
        return ",".join(map(str, value))

    def join_subvalues(self, subvalue):
        return ",".join(map(self.join_values, subvalue))

    def join_subsubvalues(self, subsubvalue):
        return ",".join(map(self.join_subvalues, subsubvalue))

    def join_subsubsubvalues(self, subsubsubvalue):
        return ",".join(map(self.join_subsubvalues, subsubsubvalue))

    def set_config_dict_dict_dict_dict_int(self, section, key, value):
        self.config[section][key] = self.join_subsubsubvalues(value)
        self.logger.info("Config: " + str(self.config))

def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_int("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
