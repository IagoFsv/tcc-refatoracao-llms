def parse_config_value(value):
    return map(lambda x: map(lambda y: map(lambda z: map(float, z.split(",")), y.split(",")), x.split(",")), value.split(","))


def materializar(valor):
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
    return materializar(parse_config_value(config.get_config_section_key_dict_dict_dict_float("mundo", "regioes")))
