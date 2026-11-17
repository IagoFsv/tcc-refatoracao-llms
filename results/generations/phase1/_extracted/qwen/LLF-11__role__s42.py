"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def split_and_map(value, delimiter):
    return map(lambda x: split_and_map(x, delimiter), value.split(delimiter)) if isinstance(value, str) else value

def split_and_map_list(value, delimiter):
    return [_materialize(item) for item in split_and_map(value, delimiter)]

class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        return split_and_map_list(split_and_map_list(split_and_map_list(self.config[section][key], ","), ","), ",")

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
    config.config["world"] = {"regions": text}
    return _materialize(config.get_config_section_key_dict_dict_dict_list("world", "regions"))
