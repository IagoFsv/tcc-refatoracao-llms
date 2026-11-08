class Config(object):
    # ...

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        config_key_dict_dict = self.get_config_section_key_dict_dict(section, key)
        return list(map(lambda x: list(map(lambda y: list(map(lambda z: z.split(","), y.split(","))), x.split(","))), config_key_dict_dict))

    # ...

def executar(texto):
    config = Config()
    config.config["mundo"] = {"regioes": texto}
    return _materializar(config.get_config_section_key_dict_dict_dict_list("mundo", "regioes"))
