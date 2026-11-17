"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_list(self, section, key):
        config_values = self.config[section][key].split(",")
        return list(map(lambda x: list(map(lambda y: list(map(lambda z: z.split(","), y.split(","))), x.split(","))), config_values))

    def get_config_section_key_dict(self, section, key):
        return self.config[section][key]

    def set_config_section_key(self, section, key, value):
        self.config[section][key] = value

    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = config


def _materialize(value):
    """Converts nested sequences (including iterators) into lists."""
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
    config.set_config_section_key("world", "regions", text)
    return _materialize(config.get_config_section_key_dict("world", "regions"))
