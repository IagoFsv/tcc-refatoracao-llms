"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_list(self, section, key):
        return map(lambda x: map(lambda y: map(lambda z: map(lambda w: w.split(","), z.split(",")), y.split(",")), x.split(",")), self.config[section][key].split(","))


def _materialize(value):
    """Converts nested sequences  (including iterators) into lists."""
    if isinstance(value, str):
        return value
    try:
        items = iter(value)
    except TypeError:
        return value
    return [ _materialize(item) for item in items]


def split_values(value, splitter):
    """Splits a value into a list of values, using a specified splitter."""
    return [split_values(item, splitter) if isinstance(item, str) and splitter in item else item for item in value.split(splitter)]


def run(text):
    """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {"regions": text}
    return _materialize(split_values(config.get_config_section_key_dict_dict_dict_list("world", "regions"), ","))
