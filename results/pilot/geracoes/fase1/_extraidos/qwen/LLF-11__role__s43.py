def split_by_comma(text):
    return list(filter(None, text.split(",")))

def materializar(valor):
    """Converte sequencias aninhadas (inclusive iteradores) em listas."""
    if isinstance(valor, str):
        return valor
    try:
        itens = iter(valor)
    except TypeError:
        return valor
    return [materializar(item) for item in itens]

def get_config_section_key_dict_dict_dict_list(config, section, key):
    return list(map(materializar, split_by_comma(config[section][key])))

def executar(texto):
    """Le o texto gravado na configuracao, como listas. Ponto de entrada publico desta unidade."""
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return get_config_section_key_dict_dict_dict_list(config.config, "mundo", "regioes")
