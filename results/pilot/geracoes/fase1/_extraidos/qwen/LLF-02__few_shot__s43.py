import logging

class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        def join_values(z):
            return ",".join(z)

        def join_lists(y):
            return ",".join(join_values(z) for z in y)

        def join_dicts(x):
            return ",".join(join_lists(y) for y in x)

        self.config[section][key] = ",".join(join_dicts(x) for x in value)
        self.logger.info("Config: " + str(self.config))


def executar(valor):
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
