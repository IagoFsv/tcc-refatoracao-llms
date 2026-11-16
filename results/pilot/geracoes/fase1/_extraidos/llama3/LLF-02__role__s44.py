import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = ",".join(map(self.join_values, value))

    def join_values(self, values):
        return ",".join(map(lambda y: ",".join(map(lambda z: ",".join(z), y)), values))

    def executar(self, valor):
        self.config["mundo"] = {}
        self.set_config_dict_dict_dict_list("mundo", "regioes", valor)
        return self.config["mundo"]["regioes"]


def main():
    config = Config()
    print(config.executar(["regiao1", ["subregiao1", ["subsubregiao1", "subsubregiao2"]], "regiao2"]))


if __name__ == "__main__":
    main()
