def parse_config_value(value):
    return map(lambda x: map(lambda y: map(lambda z: map(bool, z.split(",")), y.split(",")), x.split(",")), value.split(","))


def _materializar(valor):
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [_materializar(item) for item in itens]


def executar(texto):
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(parse_config_value(config.config["mundo"]["regioes"]))
