import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = ",".join(map(serialize_value, value))

    def serialize_value(self, value):
        return ",".join(map(serialize_value, value))

    def deserialize_value(self, value):
        return [list(map(deserialize_value, value.split(',')))]

    def deserialize_value2(self, value):
        return list(map(deserialize_value, value.split(',')))

    def deserialize_value3(self, value):
        return list(map(deserialize_value, value.split(',')))

    def executar(self, valor):
        """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
        config = self
        config.config["mundo"] = {}
        config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
        return config.config["mundo"]["regioes"]


def deserialize_value(value):
    return value


executar(["a", "b", "c"])
