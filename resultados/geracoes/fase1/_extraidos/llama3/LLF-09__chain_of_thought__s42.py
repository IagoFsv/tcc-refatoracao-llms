class Config(object):
    def __init__(self):
        self.config = {}

    def _process_config_value(self, value):
        if isinstance(value, str):
            return value
        try:
            return list(map(self._process_config_value, iter(value)))
        except TypeError:
            return value

    def _get_config_section_key_dict_dict_dict_float(self, section, key):
        config_values = self.config[section][key]
        return self._process_config_value(config_values)

    def executar(self, texto):
        self.config["mundo"] = {"regioes": texto}
        return self._get_config_section_key_dict_dict_float("mundo", "regioes")
