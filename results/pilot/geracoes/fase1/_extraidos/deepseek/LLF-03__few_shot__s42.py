"""Gravacao de valores aninhados na configuracao do jogo, como texto.

Ponto de entrada publico: executar(valor). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import logging


class Config(object):
    def  __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict(self, section, key, value):
        self.config[section][key] = self.join_values(value)
        self.logger.info("Config: " + str(self.config))

    def join_values(self, value):
        return ",".join(map(self.join_values_in_list, value))

    def join_values_in_list(self, value):
        return ",".join(map(self.join_values_in_tuple, value))

    def join_values_in_tuple(self, value):
        return ",".join(value)


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
