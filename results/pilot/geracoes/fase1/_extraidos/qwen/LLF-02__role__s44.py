import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = ",".join(self.join_lists(value))
        self.logger.info("Config: " + str(self.config))

    def join_lists(self, nested_list):
        return [",".join(map(lambda x: ",".join(map(lambda y: ",".join(y), x)), nested_list))]

def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
