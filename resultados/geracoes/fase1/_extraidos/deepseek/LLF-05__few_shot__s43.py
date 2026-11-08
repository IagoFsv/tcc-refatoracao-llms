"""Gravacao de valores aninhados na configuracao do jogo, como texto.

Ponto de entrada publico: executar(valor). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import logging


class Config(object):
    def  __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_dict_float(self, section, key, value):
        self.config[section][key] = self.join_values(value)
        self.logger.info("Config: " + str(self.config))

    def join_values(self, value):
        return ",".join(map(self.join_values_helper, value))

    def join_values_helper(self, value):
        return ",".join(map(self.join_values_helper_helper, value))

    def join_values_helper_helper(self, value):
        return ",".join(map(self.join_values_helper_helper_helper, value))

    def join_values_helper_helper_helper(self, value):
        return ",".join(map(str, value))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_dict_float("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
