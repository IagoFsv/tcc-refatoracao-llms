import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = ",".join(self.join_values(value))
        self.logger.info("Config: " + str(self.config))

    def join_values(self, value):
        return map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(z), y)), x)), value)


def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
