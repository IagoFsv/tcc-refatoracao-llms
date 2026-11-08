import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = [format_string(x) for x in value]
        self.logger.info("Config: " + str(self.config))

    def format_string(strings):
        return ",".join(",".join(",".join(z) for z in y) for y in strings)

def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
