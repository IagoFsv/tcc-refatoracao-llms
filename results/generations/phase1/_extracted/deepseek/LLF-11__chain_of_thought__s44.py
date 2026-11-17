"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def  __init__(self):
        self.config  = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        return self.map_values(self.config[section][key], self.split_by_commas)

    def map_values(self, value, func):
        return map(lambda x: map(lambda y: map(lambda z: map(lambda w: func(w, ","), z.split(",")), y.split(",")), x.split(",")), value.split(","))

    def split_by_commas(self, value, delimiter):
        return value.split(delimiter)


def _materialize(value):
    """Converts nested sequences  (including iterators) into lists."""
    if isinstance(value, str):
        return value
    try:
        items  = iter(value)
    except TypeError:
        return value
    return [_materialize(item) for item in items]


def run(text):
    """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
    config  = Config()
    config.config["world"]  = {"regions": text}
    return _materialize(config.get_config_section_key_dict_dict_dict_list("world", "regions"))
