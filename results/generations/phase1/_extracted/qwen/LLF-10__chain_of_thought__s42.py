"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def split_and_convert_to_bool(value):
    """Splits the value by commas and converts each element to a boolean."""
    return map(bool, value.split(","))

def process_nested_values(value):
    """Processes nested values by splitting and converting to boolean."""
    return map(split_and_convert_to_bool, value.split(","))

def _materialize(value):
    """Converts nested sequences (including iterators) into lists."""
    if isinstance(value, str):
        return value
    try:
        items = iter(value)
    except TypeError:
        return value
    return [_materialize(item) for item in items]


class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_bool(self, section, key):
        """Processes nested values stored in the configuration."""
        return map(process_nested_values, self.config[section][key].split(","))


def run(text):
    """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {"regions": text}
    return _materialize(config.get_config_section_key_dict_dict_dict_bool("world", "regions"))
