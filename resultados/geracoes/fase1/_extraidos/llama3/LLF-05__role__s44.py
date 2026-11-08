import logging


class Config(object):
    def __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = ",".join(map(self.join_values, value))

    def join_values(self, values):
        return ",".join(map(self.join_values, map(self.join_values, values)))

    def executar(self, valor):
        self.config["mundo"] = {}
        self.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
        return self.config["mundo"]["regioes"]


def main():
    config = Config()
    print(config.executar([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]))


if __name__ == "__main__":
    main()
