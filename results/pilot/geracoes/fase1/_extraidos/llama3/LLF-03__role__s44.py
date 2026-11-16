import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(z), y)), x)), value))
        self.logger.info("Config: " + str(self.config))

    def format_value(self, x):
        return ",".join(map(lambda y: ",".join(map(lambda z: ",".join(z), y)), x))

    def executar(self, valor):
        self.config["mundo"] = {}
        self.config["mundo"]["regioes"] = self.format_value(valor)
        return self.config["mundo"]["regioes"]


def executar(valor):
    config = Config()
    return config.executar(valor)
