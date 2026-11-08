import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def serialize_value(self, value):
        return ",".join(map(str, value))

    def serialize_layer(self, layer):
        return ",".join(map(self.serialize_value, layer))

    def serialize_section(self, section):
        return ",".join(map(self.serialize_layer, section))

    def serialize_config(self, config):
        return ",".join(map(self.serialize_section, config))

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = self.serialize_config(value)
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
