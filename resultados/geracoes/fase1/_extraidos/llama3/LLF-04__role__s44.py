import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_int(self, section, key, value):
        self.config[section][key] = ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(map(str, z)), y)), x)), value))
        self.logger.info("Config: " + str(self.config))

    def process_value(self, value):
        return ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(map(str, z)), y)), x)), value))

    def executar(self, valor):
        self.config["mundo"] = {}
        self.config["mundo"]["regioes"] = self.process_value(valor)
        return self.config["mundo"]["regioes"]


def executar(valor):
    config = Config()
    return config.executar(valor)
