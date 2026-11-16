import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = map(self.format_string, value)
        self.logger.info("Config: " + str(self.config))

    def format_string(self, x):
        return ",".join(",".join(",".join(z) for z in y) for y in x)

def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
