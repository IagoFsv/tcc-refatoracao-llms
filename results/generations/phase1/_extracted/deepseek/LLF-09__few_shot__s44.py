"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return map(lambda x: map(lambda y: map(lambda z: map(float, z.split(",")), y.split(",")), x.split(",")), self.config[section][key].split(","))


def _materialize(value):
    """Converts nested sequences  (including iterators) into lists."""
    if isinstance(value, str):
        return value
    try:
        items = iter(value)
    except TypeError:
        return value
    return [ _materialize(item) for item in items]


def parse_value(value):
    return map(lambda y: map(lambda z: map(float, z.split(",")), y.split(",")), value.split(","))


def run(text):
    """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {"regions": text}
    return _materialize(parse_value(config.config["world"]["regions"]))
