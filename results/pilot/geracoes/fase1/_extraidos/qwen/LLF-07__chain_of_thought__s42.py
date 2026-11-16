Leitura de valores aninhados da configuracao do jogo, gravados como texto.

Ponto de entrada publico: executar(texto). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict(self, section, key):
        return self._process_nested_strings(self.config[section][key].split(","))

    def _process_nested_strings(self, nested_strings):
        return map(self._process_string, nested_strings)

    def _process_string(self, s):
        return map(self._process_string, s.split(","))

    def _materializar(self, valor):
        """Converte sequencias aninhadas (inclusive iteradores) em listas."""
        if isinstance(valor, str):
            return valor
        try:
            itens = iter(valor)
        except TypeError:
            return valor
        return [self._materializar(item) for item in itens]


def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return config._materializar(config.get_config_section_key_dict_dict_dict("mundo", "regioes"))
