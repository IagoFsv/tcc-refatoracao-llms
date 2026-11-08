def split_by_comma(value):
    return value.split(",")

def materializar(valor):
    """Converte sequencias aninhadas (inclusive iteradores) em listas."""
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [_materializar(item) for item in itens]

def get_config_section_key_dict_dict_list(config, section, key):
    return map(lambda x: map(lambda y: map(lambda z: z.split(","), y.split(",")), x.split(",")), config[section][key].split(","))

def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return materializar(get_config_section_key_dict_dict_list(config, "mundo", "regioes"))
