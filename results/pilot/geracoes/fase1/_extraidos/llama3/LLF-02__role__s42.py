import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(z), y)), x)), value))
        self.logger.info("Config: " + str(self.config))

    def format_value(self, value):
        return ",".join(map(lambda x: ",".join(map(lambda y: ",".join(map(lambda z: ",".join(z), y)), x)), value))

    def executar(self, valor):
        """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
        self.config["mundo"] = {}
        self.config["mundo"]["regioes"] = self.format_value(valor)
        return self.config["mundo"]["regioes"]

def main():
    config = Config()
    print(config.executar(["regiao1", ["subregiao1", ["subsubregiao11", "subsubregiao12"]], "subregiao2"]))

if __name__ == "__main__":
    main()
