"""Reads nested values stored as text in the game configuration.

Public entry point: run(text). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def parse_nested_values(value):
    """Parses nested values from a string."""
    return map(float, value.split(","))

def convert_to_list(value):
    """Converts nested sequences (including iterators) into lists."""
    if isinstance(value, str):
        return value
    try:
        items = iter(value)
    except TypeError:
        return value
    return [convert_to_list(item) for item in items]

class Config(object):
    def __init__(self):
        self.config = {}

    def get_config_section_key_dict_dict_dict_float(self, section, key):
        nested_values = self.config[section][key].split(",")
        parsed_values = parse_nested_values(nested_values[0])
        for value in nested_values[1:]:
            parsed_values = map(parse_nested_values, parsed_values)
        return parsed_values

def _materialize(value):
    """Converts nested sequences (including iterators) into lists."""
    return convert_to_list(value)

def run(text):
    """Reads the stored text from the configuration, as lists. Public entry point of this unit."""
    config = Config()
    config.config["world"] = {"regions": text}
    return _materialize(config.get_config_section_key_dict_dict_dict_float("world", "regions"))
