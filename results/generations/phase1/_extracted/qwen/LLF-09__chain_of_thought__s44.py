"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        return self._process_nested_values(self.config[section][key].split(","))

    def _process_nested_values(self, values):
        return map(self._process_third_level, values)

    def _process_third_level(self, value):
        return map(self._process_second_level, value.split(","))

    def _process_second_level(self, value):
        return map(self._process_first_level, value.split(","))

    def _process_first_level(self, value):
        return float(value.split(","))


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
    return _materialize(config.get_config_section_key_dict_dict_dict_float("world", "regions"))
