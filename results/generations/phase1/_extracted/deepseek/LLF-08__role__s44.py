"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_int(self, section, key):
        return map(self._lambda_to_named_function, self.config[section][key].split(","))

    def _lambda_to_named_function(self, x):
        return map(self._lambda_to_named_function, x.split(","))

    def _lambda_to_named_function(self, y):
        return map(self._lambda_to_named_function, y.split(","))

    def _lambda_to_named_function(self, z):
        return map(int, z.split(","))


def _materialize(value):
    """Converts nested sequences (including iterators) into lists."""
    if isinstance(value, str):
        return value
    try:
        items = iter(value)
    except TypeError:
        return value
    return [ _materialize(item) for item in items]


def run(text):
    """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {"regions": text}
    return _materialize(config.get_config_section_key_dict_dict_dict_int("world", "regions"))
