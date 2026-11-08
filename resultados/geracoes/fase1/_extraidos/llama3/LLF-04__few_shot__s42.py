class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def _format_value(self, value):
        return ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(map(str, z)), y)), x)), value))

    def set_config_dict_dict_dict_dict_int(self, section, key, value):
        self.config[section][key] = self._format_value(value)
        self.logger.info("Config: " + str(self.config))

    def executar(self, valor):
        self.config["mundo"] = {}
        self.set_config_dict_dict_dict_dict_int("mundo", "regioes", valor)
        return self.config["mundo"]["regioes"]
