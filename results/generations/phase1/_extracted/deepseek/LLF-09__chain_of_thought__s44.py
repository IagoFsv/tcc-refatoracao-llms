class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return self.map_values(self.config[section][key])

    def map_values(self, value):
        return map(self.map_values, value.split(","))

    def map_values_2(self, value):
        return map(self.map_values_2, value.split(","))

    def map_values_3(self, value):
        return map(self.map_values_3, value.split(","))

    def map_values_4(self, value):
        return map(float, value.split(","))

def _materialize(value):
    """Converts nested sequences  (including iterators) into lists."""
    if isinstance(value, str):
        return value
    try:
        items = iter(value)
    except TypeError:
        return value
    return [_materialize(item) for item in items]


def run(text):
    """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {"regions": text}
    return _materialize(config.get_config_section_key_dict_dict_dict_float("world", "regions"))
