import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_int(self, section, key, value):
        def format_value(x):
            return ",".join(",".join(",".join(map(str, z)) for z in y) for y in x)
        self.config[section][key] = format_value(value)
        self.logger.info("Config: " + str(self.config))

    def executar(self, valor):
        config = self
        config.config["mundo"] = {}
        config.set_config_dict_dict_dict_dict_int("mundo", "regioes", valor)
        return config.config["mundo"]["regioes"]


def main():
    config = Config()
    valor = [...]  # valor a ser gravado
    print(config.executar(valor))


if __name__ == "__main__":
    main()
