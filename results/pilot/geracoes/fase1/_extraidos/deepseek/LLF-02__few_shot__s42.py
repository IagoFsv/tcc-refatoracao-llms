"""Gravacao de valores aninhados na configuracao do jogo, como texto.

Ponto de entrada publico: executar(valor). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import logging


class Config(object):
    def  __init__(self):
        self.config = {}
        self.logger = logging.getLogger(__name__)

    def set_config_dict_dict_dict_list(self, section, key, value):
        self.config[section][key] = ",".join(map(transformar_valores, value))
        self.logger.info("Config: " + str(self.config))


def transformar_valores(valores):
    return ",".join(map(transformar_valores, valores))


def executar(valor):
    """Grava valor na configuracao e devolve o texto gravado. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {}
    config.set_config_dict_dict_dict_list("mundo", "regioes", valor)
    return config.config["mundo"]["regioes"]
