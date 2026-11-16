class Config(object):
    def __init__(self):
        self.config = {}

    def _get_config_value(self, section, key):
        return self.config[section][key]

    def _map_to_bool(self, value):
        return bool(value.split(','))

    def _map_list_to_list(self, values):
        return list(map(lambda x: list(map(self._map_to_bool, x.split(','))), values.split(',')))

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        config_values = self._get_config_value(section, key)
        return self._map_list_to_list(config_values)

    def executar(self, texto):
        self.config["mundo"] = {"regioes": texto}
        return _materializar(self.get_config_section_key_dict_dict_dict_bool("mundo", "regioes"))
