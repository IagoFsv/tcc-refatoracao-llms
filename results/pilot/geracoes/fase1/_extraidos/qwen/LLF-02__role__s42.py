import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def flatten_and_join(self, data):
        return ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(z), y)), x)), data))

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = self.flatten_and_join(value)
        self.logger.info("Config: " + str(self.config))

def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
